import time
import os
import queue
import threading
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from rich.console import Console
from core.config import RAW_DOCS_DIR, PARSED_DOCS_DIR, get_watch_dirs
from core.parser import parse_document, SUPPORTED_EXTENSIONS
from core.factories import initialize_system
from tqdm import tqdm
from core.i18n import t

console = Console(stderr=True)

# Global task queue for asynchronous parsing
task_queue = queue.Queue()
_last_modified_times = {}
DEBOUNCE_SECONDS = 2.0

def _worker_loop(context_manager):
    """Background worker to process files from the queue."""
    try:
        while True:
            try:
                action, file_path = task_queue.get()
                if action == "stop":
                    task_queue.task_done()
                    break
                
                path = Path(file_path)
                if action == "deleted":
                    console.print(t("watch_del", name=path.name))
                    context_manager.delete_context(path.name)
                elif action in ["created", "modified"]:
                    content, error = parse_document(path)
                    if content:
                        console.print(f"[green]✅ {path.name}[/green]")
                        if path.suffix.lower() not in ['.md', '.txt']:
                            parsed_path = PARSED_DOCS_DIR / f"{path.stem}.md"
                            with open(parsed_path, "w", encoding="utf-8") as f:
                                f.write(content)
                        context_manager.write_context(path.name, content, level="L2")
                    else:
                        console.print(f"[red]❌ {path.name}[/red] [dim]{error}[/dim]")
            except Exception as e:
                console.print(f"[bold red]Error processing {file_path}: {e}[/bold red]")
                import traceback
                traceback.print_exc()
            finally:
                task_queue.task_done()
    except Exception as e:
        console.print(f"[bold red]Worker thread fatal error: {e}[/bold red]")
        import traceback
        traceback.print_exc()

class DocumentHandler(FileSystemEventHandler):
    def __init__(self, context_manager):
        self.context_manager = context_manager

    def _queue_task(self, file_path, event_type):
        path = Path(file_path)
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return

        # Debounce logic for modify/create events
        if event_type in ["created", "modified"]:
            current_time = time.time()
            last_time = _last_modified_times.get(str(path), 0)
            if current_time - last_time < DEBOUNCE_SECONDS:
                return  # Ignore event, debounced
            _last_modified_times[str(path)] = current_time

        if event_type == "deleted":
            _last_modified_times.pop(str(path), None)
        else:
            ev_map = {"created": "create", "modified": "modify", "deleted": "delete"}
            ev_str = t(f"watch_ev_{ev_map.get(event_type, event_type)}")
            console.print(t("watch_event", event=ev_str, name=path.name))
            
        task_queue.put((event_type, file_path))

    def on_created(self, event):
        if not event.is_directory:
            self._queue_task(event.src_path, "created")

    def on_modified(self, event):
        if not event.is_directory:
            self._queue_task(event.src_path, "modified")

    def on_deleted(self, event):
        if not event.is_directory:
            self._queue_task(event.src_path, "deleted")

def index_dir(directory: Path):
    """Index a single directory and show progress."""
    context_manager = initialize_system()
    all_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            path = Path(root) / f
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                all_files.append(path)

    if not all_files:
        console.print(t("idx_no_files"))
        return

    console.print(t("idx_found", count=len(all_files)))
    for path in tqdm(all_files, desc=t("idx_progress"), unit="file"):
        content, error = parse_document(path)
        if content:
            if path.suffix.lower() not in ['.md', '.txt']:
                parsed_path = PARSED_DOCS_DIR / f"{path.stem}.md"
                with open(parsed_path, "w", encoding="utf-8") as f:
                    f.write(content)
            context_manager.write_context(path.name, content, level="L2")
            tqdm.write(f"✅ {path.name}")
        else:
            tqdm.write(f"❌ {path.name}  {error}")
    console.print(t("idx_complete"))

def index_all():
    context_manager = initialize_system()
    watch_dirs = get_watch_dirs()
    
    all_files = []
    local_filenames = set()
    for d in watch_dirs:
        for root, _, files in os.walk(d):
            for f in files:
                path = Path(root) / f
                if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    all_files.append(path)
                    local_filenames.add(path.name)
                    
    # Clean up ghost data
    indexed_filenames = context_manager.get_all_filenames()
    ghost_files = [f for f in indexed_filenames if f not in local_filenames]
    if ghost_files:
        console.print(t("idx_ghost_clean", count=len(ghost_files)))
        for f in ghost_files:
            context_manager.delete_context(f)

    if not all_files:
        console.print(t("idx_no_files"))
        return

    console.print(t("idx_found", count=len(all_files)))
    for path in tqdm(all_files, desc=t("idx_progress"), unit="file"):
        content, error = parse_document(path)
        if content:
            # Only save to parsed_docs if conversion was needed (not .md or .txt)
            if path.suffix.lower() not in ['.md', '.txt']:
                parsed_path = PARSED_DOCS_DIR / f"{path.stem}.md"
                with open(parsed_path, "w", encoding="utf-8") as f:
                    f.write(content)
            context_manager.write_context(path.name, content, level="L2")
            tqdm.write(f"✅ {path.name}")
        else:
            tqdm.write(f"❌ {path.name}  {error}")
    console.print(t("idx_complete"))

def start_watching():
    try:
        context_manager = initialize_system()
    except Exception as e:
        console.print(f"[bold red]Failed to initialize system: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        return
    
    # Start worker thread for async parsing
    worker_thread = threading.Thread(target=_worker_loop, args=(context_manager,), daemon=True)
    worker_thread.start()
    
    event_handler = DocumentHandler(context_manager)
    observer = PollingObserver(timeout=2)  # Fork-safe observer with 2-second polling interval
    
    watched_dirs = set()

    def schedule_new_dirs():
        try:
            for d in get_watch_dirs():
                d = Path(d)
                if str(d) not in watched_dirs:
                    d.mkdir(parents=True, exist_ok=True)
                    observer.schedule(event_handler, str(d), recursive=True)
                    console.print(t("watch_dir", dir=d))
                    watched_dirs.add(str(d))
        except Exception as e:
            console.print(f"[bold red]Error scheduling watch directories: {e}[/bold red]")
            import traceback
            traceback.print_exc()

    schedule_new_dirs()
    observer.start()
    try:
        while True:
            time.sleep(5)
            schedule_new_dirs()  # Periodically check for newly added watch dirs
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
        observer.stop()
        task_queue.put(("stop", None))
    except Exception as e:
        console.print(f"[bold red]Error in watch loop: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        observer.stop()
        task_queue.put(("stop", None))
    finally:
        observer.join()
        console.print("[green]✅ ContextBridge watcher stopped.[/green]")

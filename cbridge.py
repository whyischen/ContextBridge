#!/usr/bin/env python3
import sys
import click
import asyncio
import os
import shutil
from pathlib import Path
from rich.console import Console

from core.factories import initialize_system
from core.config import (
    init_workspace, CONFIG, WORKSPACE_DIR, CONFIG_PATH, save_config, 
    get_watch_dirs, add_watch_dir, remove_watch_dir
)
from core.watcher import start_watching, index_all, index_dir
from core.mcp_server import main as mcp_main
from core.i18n import t
from core.utils.process import (
    is_process_running, stop_process_by_file, 
    start_background_process, get_pid_from_file
)
from core.utils.logger import setup_logger

console = Console(stderr=True)

# ============================================================================
# 常量定义
# ============================================================================
CBRIDGE_HOME = Path.home() / ".cbridge"
PID_FILE_SERVE = CBRIDGE_HOME / "cbridge.pid"
PID_FILE_WATCHER = CBRIDGE_HOME / "cbridge_watcher.pid"
LOG_DIR = CBRIDGE_HOME / "logs"
LOG_FILE_WATCHER = LOG_DIR / "cbridge-watcher.log"
LOG_FILE_SERVE = LOG_DIR / "cbridge-serve.log"

def _display_index_summary(result, quiet=False):
    """Display indexing summary results"""
    if quiet:
        return
    
    console.print()
    console.print(t("idx_summary", success=result['success'], failed=result['failed']))
    
    if result['failed'] > 0 and result.get('failed_files'):
        console.print()
        console.print(t("failed_files_header"))
        for item in result['failed_files'][:5]:
            console.print(f"  [red]•[/red] {item['file']}: {item['error'][:100]}")
        if len(result['failed_files']) > 5:
            console.print(t("and_more", count=len(result['failed_files']) - 5))

def get_version():
    try:
        import importlib.metadata
        return importlib.metadata.version('cbridge-agent')
    except Exception:
        return 'unknown'

@click.group(help=t("cli_desc"))
@click.version_option(version=get_version(), prog_name="ContextBridge")
def cli():
    pass

@cli.command(help=t("init_desc"))
def init():
    console.print(t("init_welcome"))
    
    if CONFIG_PATH.exists():
        console.print(t("init_config_exists", path=CONFIG_PATH.absolute()))
        if click.confirm(t("init_config_delete_confirm"), default=True):
            CONFIG_PATH.unlink()
            if WORKSPACE_DIR.exists():
                if click.confirm(t("init_workspace_delete_confirm", dir=WORKSPACE_DIR), default=False):
                    shutil.rmtree(WORKSPACE_DIR)
        else:
            return
    
    # Stop any running services
    stop_process_by_file(PID_FILE_WATCHER)
    stop_process_by_file(PID_FILE_SERVE)
    
    # Interactive configuration
    lang = click.prompt(t("choose_lang"), type=click.Choice(['zh', 'en']), default='en')
    workspace = click.prompt(t("workspace_dir"), default="~/.cbridge/workspace")
    
    config_data = {
        "mode": "embedded", 
        "language": lang, 
        "watch_dirs": [],
        "workspace_dir": workspace
    }
    
    save_config(config_data)
    init_workspace()
    
    # Start daemon automatically
    cmd = [sys.executable, "-m", "cbridge", "start", "--foreground"]
    pid = start_background_process(cmd, PID_FILE_WATCHER, LOG_FILE_WATCHER)
    
    if pid > 0:
        console.print(t("watcher_started_bg", pid=pid))
        console.print(t("init_complete"))

@cli.group(help=t("watch_desc"))
def watch():
    pass

@watch.command(name="list", help=t("watch_list_desc"))
def watch_list():
    dirs = get_watch_dirs()
    console.print(t("watch_list_title"))
    for d in dirs:
        console.print(f"  [green]•[/green] {d}")

@watch.command(name="add", help=t("watch_add_desc"))
@click.argument("path")
@click.option('--no-index', is_flag=True)
@click.option('--quiet', '-q', is_flag=True)
@click.option('--background', '-b', is_flag=True)
def watch_add(path, no_index, quiet, background):
    target_path = Path(os.path.expanduser(path)).absolute()
    if not target_path.exists():
        console.print(t("watch_add_not_exist", path=path))
        sys.exit(1)
        
    if add_watch_dir(path):
        console.print(t("watch_add_success", path=path))
        if no_index: return
        
        if not background:
            console.print(t("watch_add_scanning"))
            result = index_dir(target_path, show_progress=not quiet, skip_scan_log=True)
            _display_index_summary(result, quiet)
        else:
            console.print(t("watch_add_starting_background"))
            cmd = [sys.executable, "-m", "cbridge", "index", "--path", str(target_path)]
            if quiet: cmd.append("--quiet")
            start_background_process(cmd, CBRIDGE_HOME / f"index_{target_path.stem}.pid", LOG_FILE_WATCHER)
            console.print(t("watch_add_background_started"))
    else:
        console.print(t("watch_add_exists", path=path))

@watch.command(name="remove", help=t("watch_remove_desc"))
@click.argument("path")
@click.option('--skip-cleanup', is_flag=True)
def watch_remove(path, skip_cleanup):
    if not remove_watch_dir(path):
        console.print(t("watch_remove_not_found", path=path))
        return
    
    console.print(t("watch_remove_success", path=path))
    if not skip_cleanup:
        console.print(t("cleanup_background"))
        # Cleanup logic could be a separate background task or handled by watcher
        # For simplicity, we just trigger a full re-index or trust the watcher to sync
        pass

@cli.command(help=t("index_desc"))
@click.option('--path', help='Index specific path')
@click.option('--quiet', '-q', is_flag=True)
def index(path, quiet):
    if path:
        result = index_dir(Path(path), show_progress=not quiet)
        _display_index_summary(result, quiet)
    else:
        console.print(t("index_start"))
        index_all()

@cli.command(help=t("start_desc"))
@click.option('--foreground', is_flag=True)
def start(foreground):
    if not foreground:
        cmd = [sys.executable, "-m", "cbridge", "start", "--foreground"]
        pid = start_background_process(cmd, PID_FILE_WATCHER, LOG_FILE_WATCHER)
        if pid > 0:
            console.print(t("watcher_started_bg", pid=pid))
            return
    
    console.print(t("start_init"))
    init_workspace()
    console.print(t("watcher_running_fg"))
    start_watching()

@cli.command(help=t("serve_desc"))
@click.option('--port', default=9790)
@click.option('--host', default='127.0.0.1')
@click.option('--foreground', is_flag=True)
def serve(port, host, foreground):
    import uvicorn
    import threading
    
    # Check if already running
    current_pid = get_pid_from_file(PID_FILE_SERVE)
    if current_pid and is_process_running(current_pid):
        console.print(t("api_already_running", pid=current_pid))
        sys.exit(1)
        
    if not foreground:
        cmd = [sys.executable, "-m", "cbridge", "serve", "--host", host, "--port", str(port), "--foreground"]
        pid = start_background_process(cmd, PID_FILE_SERVE, LOG_FILE_SERVE)
        if pid > 0:
            console.print(t("serve_daemon_start", pid=pid))
            console.print(t("serve_daemon_url", host=host, port=port))
            sys.exit(0)
    
    # Foreground logic
    init_workspace()
    watcher_thread = threading.Thread(target=start_watching, daemon=True)
    watcher_thread.start()
    uvicorn.run("core.api_server:app", host=host, port=port, log_level="info")

@cli.command(help=t("stop_desc"))
def stop():
    stopped = False
    for name, pid_file in [("Watcher", PID_FILE_WATCHER), ("API Server", PID_FILE_SERVE)]:
        pid = get_pid_from_file(pid_file)
        if pid:
            if stop_process_by_file(pid_file):
                console.print(f"✅ {name} stopped (PID: {pid})")
                stopped = True
    if not stopped:
        console.print(t("no_daemon_found"))

@cli.command(help=t("status_desc"))
def status():
    console.print(t("status_title"))
    console.print(t("status_lang", lang=CONFIG.get('language', 'zh')))
    console.print(t("status_workspace", workspace=WORKSPACE_DIR))
    
    for name, pid_file in [("Watcher", PID_FILE_WATCHER), ("API Server", PID_FILE_SERVE)]:
        pid = get_pid_from_file(pid_file)
        if pid and is_process_running(pid):
            console.print(f"✅ {name}: [green]Running[/green] (PID: {pid})")
        else:
            console.print(f"❌ {name}: [red]Not Running[/red]")

@cli.command(help=t("logs_desc"))
@click.option('--type', '-t', type=click.Choice(['watcher', 'serve']), default='watcher')
@click.option('--lines', '-n', default=50)
@click.option('--follow', '-f', is_flag=True)
def logs(type, lines, follow):
    import time
    log_file = LOG_FILE_WATCHER if type == 'watcher' else LOG_FILE_SERVE
    if not log_file.exists():
        console.print(t("logs_not_found", file=log_file))
        return
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            if follow:
                lines_list = f.readlines()
                for line in lines_list[-lines:]: print(line.rstrip())
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line: print(line.rstrip())
                    else: time.sleep(0.1)
            else:
                for line in f.readlines()[-lines:]: print(line.rstrip())
    except KeyboardInterrupt:
        pass

@cli.command(help=t("search_desc"))
@click.argument('query')
@click.option('--top-k', type=int)
@click.option('--threshold', type=float)
@click.option('--explain', is_flag=True)
def search(query, top_k, threshold, explain):
    from core.config import get_watch_dirs, PARSED_DOCS_DIR
    from core.utils.path_resolver import PathResolver
    
    context_manager = initialize_system()
    results = context_manager.recursive_retrieve(
        query=query, 
        top_k=top_k or 5, 
        min_similarity=threshold or 0.5,
        explain=explain
    )
    
    if not results:
        console.print(t("search_empty"))
        return
        
    resolver = PathResolver({'watch_dirs': get_watch_dirs(), 'parsed_docs_dir': PARSED_DOCS_DIR})
    for idx, res in enumerate(results, 1):
        source = res.get('uri', 'Unknown')
        full_path = ""
        try:
            full_path = resolver.resolve_path(res.get('filename', ''), source)
        except: pass
        
        console.print(f"\n[bold cyan]#{idx}[/bold cyan] [bold]{source}[/bold] (Score: {res.get('score', 0):.2f})")
        if full_path: console.print(f"  📂 Path: {full_path}")
        if explain and 'score_breakdown' in res:
            b = res['score_breakdown']
            console.print(f"  📊 Breakdown: Semantic {b.get('semantic',0):.2f}, BM25 {b.get('bm25',0):.2f}")
        
        abstract = res.get('abstract', '')
        if abstract: console.print(f"  📖 Abstract: {abstract[:200]}...")
        
        for ex in res.get('relevant_excerpts', [])[:2]:
            console.print(f"  📝 Excerpt: {ex[:150]}...")

@cli.group(help="Manage search configuration")
def search_config():
    pass

@search_config.command(name="show")
def show_search_config():
    from core.config import get_search_config
    c = get_search_config()
    console.print(f"Min Similarity: {c.get('min_similarity')}")
    console.print(f"Default Top K: {c.get('top_k')}")

@search_config.command(name="set")
@click.option('--threshold', type=float)
@click.option('--top-k', type=int)
def set_search_config(threshold, top_k):
    from core.config import update_search_config
    update_search_config(min_similarity=threshold, top_k=top_k)
    console.print("Updated.")

@cli.command(help=t("config_desc"))
def config():
    if CONFIG_PATH.exists():
        console.print(CONFIG_PATH.read_text())
    else:
        console.print(t("config_not_found"))

@cli.command(help=t("mcp_desc"))
def mcp():
    asyncio.run(mcp_main())

@cli.command(help=t("lang_desc"))
@click.argument("lang", type=click.Choice(['zh', 'en']))
def lang(lang):
    CONFIG["language"] = lang
    save_config(CONFIG)
    console.print(t("lang_success", lang=lang))

if __name__ == "__main__":
    cli()

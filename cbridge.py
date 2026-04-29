#!/usr/bin/env python3
"""
ContextBridge CLI Entry Point
"""

import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.box import ROUNDED
from rich.console import Group
from pathlib import Path

from core.factories import initialize_system
from core.config import CONFIG, save_config, get_watch_dirs, PARSED_DOCS_DIR, init_workspace
from core.watcher import start_watching, list_monitored_dirs, add_monitored_dir, remove_monitored_dir, index_all_dirs
from core.mcp_server import start_mcp_server
from core.i18n import t, set_language
from core.utils.process import (
    start_background_process, stop_background_process, 
    get_process_status, WATCHER_PID_FILE
)
from core.utils.logger import setup_logger, get_logger
from core.platform import platform_compat
from core.__version__ import __version__

# Initialize logger and console
setup_logger()
logger = get_logger("cli")
console = Console()

@click.group(help=t("cli_desc"))
@click.version_option(version=__version__, prog_name="cbridge")
def cli():
    """ContextBridge CLI"""
    pass

@cli.command(help=t("init_desc"))
def init():
    """Initialize workspace and configuration"""
    console.print(t("init_welcome"))
    
    config_path = Path("config.yaml")
    if config_path.exists():
        console.print(t("init_config_exists", path=config_path))
        if click.confirm(t("init_config_delete_confirm"), default=False):
            os.remove(config_path)
            console.print(t("init_config_deleted"))
            
            # Optionally clean workspace too
            workspace_dir = Path(CONFIG.get("workspace", "workspace"))
            if workspace_dir.exists():
                if click.confirm(t("init_workspace_delete_confirm", dir=workspace_dir), default=False):
                    import shutil
                    shutil.rmtree(workspace_dir)
                    console.print(t("init_workspace_deleted"))
        else:
            console.print(t("init_cancelled"))
            return

    # Check if watcher service is running and offer to stop it
    watcher_status = get_process_status(WATCHER_PID_FILE)
    
    if watcher_status[0] == "running":
        console.print("\n[yellow]⚠️  Detected running watcher service.[/yellow]")
        if click.confirm("Stop existing watcher before re-initializing?", default=True):
            if stop_background_process(WATCHER_PID_FILE):
                console.print(t("init_stopped_watcher", pid=watcher_status[1]))
            console.print(t("init_services_stopped"))

    # Language selection
    lang = click.prompt(t("choose_lang"), type=click.Choice(['zh', 'en']), default='zh')
    set_language(lang)
    
    # Workspace selection
    workspace = click.prompt(t("workspace_dir"), default="workspace")
    
    # Update config
    CONFIG["language"] = lang
    CONFIG["workspace"] = workspace
    save_config(CONFIG)
    console.print(t("config_saved", path=config_path))
    
    # Initialize workspace
    init_workspace()
    
    # Ask about starting services
    console.print(t("init_config_prompt"))
    if click.confirm("Start ContextBridge services now?", default=True):
        console.print(t("init_starting_daemon"))
        # We start the watcher (which covers both watch and serve for simple use)
        # Using sys.executable to ensure we use the same python environment
        cmd = [sys.executable, os.path.abspath(__file__), "start", "--foreground"]
        pid = start_background_process(cmd, WATCHER_PID_FILE, "cbridge-watcher.log")
        if pid:
            console.print(t("init_complete"))
        else:
            console.print(t("init_daemon_failed", error="Unknown error"))

@cli.group(help=t("watch_desc"))
def watch():
    """Watch directory management"""
    pass

@watch.command(name="list", help=t("watch_list_desc"))
def watch_list():
    """List all monitored directories"""
    dirs = list_monitored_dirs()
    if not dirs:
        console.print("[yellow]📭 No directories monitored yet.[/yellow]")
        return
    console.print(t("watch_list_title"))
    for d in dirs:
        console.print(f"  • {d}")

@watch.command(name="add", help=t("watch_add_desc"))
@click.argument('path', type=click.Path(exists=True))
def watch_add(path):
    """Add a directory to monitor"""
    abs_path = os.path.abspath(path)
    if add_monitored_dir(abs_path):
        console.print(t("watch_add_success", path=abs_path))
    else:
        console.print(t("watch_add_exists", path=abs_path))

@watch.command(name="remove", help=t("watch_remove_desc"))
@click.argument('path')
def watch_remove(path):
    """Remove a directory from monitoring"""
    if remove_monitored_dir(path):
        console.print(t("watch_remove_success", path=path))
    else:
        console.print(t("watch_remove_not_found", path=path))

@cli.command(help=t("index_desc"))
def index():
    """Force full re-index of all monitored directories"""
    console.print(t("index_start"))
    index_all_dirs()

@cli.command(help=t("start_desc"))
@click.option('--foreground', is_flag=True, help="Run in foreground instead of background")
def start(foreground):
    """Start the ContextBridge service (Watcher + Vector DB)"""
    if foreground:
        start_watching()
    else:
        cmd = [sys.executable, os.path.abspath(__file__), "start", "--foreground"]
        pid = start_background_process(cmd, WATCHER_PID_FILE, "cbridge-watcher.log")
        if pid:
            console.print(t("watcher_started_bg", pid=pid))
            console.print(t("logs_location", path="~/.cbridge/logs/cbridge-watcher.log"))
            console.print(t("logs_view_hint"))
            console.print(t("stop_hint"))
        else:
            console.print("[red]❌ Failed to start background service.[/red]")

@cli.command(help=t("status_desc"))
def status():
    """Check services status"""
    watcher_status, watcher_pid = get_process_status(WATCHER_PID_FILE)
    
    console.print(t("status_title"))
    console.print(t("status_lang", lang=CONFIG.get("language", "en")))
    
    if watcher_status == "running":
        console.print(t("watcher_status_running", pid=watcher_pid))
    else:
        console.print(t("watcher_status_not_running"))

@cli.command(help="Stop all ContextBridge background services")
def stop():
    """Stop background services"""
    watcher_stopped = stop_background_process(WATCHER_PID_FILE)
    if watcher_stopped:
        console.print("[green]✅ Watcher stopped.[/green]")
    else:
        console.print("[dim]Watcher was not running.[/dim]")
        

@cli.command(help=t("logs_desc"))
@click.option('--follow', '-f', is_flag=True, help=t("logs_follow_help"))
@click.option('--lines', '-n', default=50, help=t("logs_lines_help"))
@click.argument('service', type=click.Choice(['watcher', 'main', 'all']), default='all')
def logs(follow, lines, service):
    """View service logs"""
    log_dir = os.path.expanduser("~/.cbridge/logs")
    
    # Determine which log files to use
    if service == 'watcher':
        log_files = ["cbridge-watcher.log"]
    elif service == 'main':
        log_files = ["cbridge.log"]
    else:  # all
        log_files = ["cbridge.log", "cbridge-watcher.log"]
    
    # Check if any log files exist
    existing_log_files = []
    for log_file in log_files:
        log_path = os.path.join(log_dir, log_file)
        if os.path.exists(log_path):
            existing_log_files.append(log_path)
    
    if not existing_log_files:
        # Try to show at least one log file if possible
        if service != 'all':
            console.print(t("logs_not_found", file=os.path.join(log_dir, log_files[0])))
        else:
            console.print(t("logs_not_found", file=log_dir))
        return
    
    if follow:
        if len(existing_log_files) == 1:
            # Single file follow mode
            log_path = existing_log_files[0]
            console.print(t("logs_follow_mode", file=log_path))
            console.print(t("logs_exit_hint"))
            try:
                import subprocess
                # Platform-specific log following command
                cmd = platform_compat.get_follow_logs_command(Path(log_path), lines)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in process.stdout:
                    print(line, end='')
            except KeyboardInterrupt:
                console.print(t("logs_stopped"))
            except Exception as e:
                console.print(t("logs_error", error=str(e)))
        else:
            # Multiple file follow mode - show last N lines and then follow the most recently modified
            console.print("[bold]Following multiple log files (showing recent entries):[/bold]")
            
            # Show recent lines from all files
            all_lines = []
            for log_path in existing_log_files:
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        file_lines = f.readlines()
                        # Add filename prefix to each line
                        for line in file_lines[-(lines//len(existing_log_files)):]:
                            all_lines.append((os.path.getmtime(log_path), f"[{os.path.basename(log_path)}] {line}"))
                except Exception:
                    continue
            
            # Sort by timestamp and display
            all_lines.sort(key=lambda x: x[0])
            for _, line in all_lines[-lines:]:
                print(line, end='')
            
            # Follow the most recently modified file
            most_recent_file = max(existing_log_files, key=os.path.getmtime)
            console.print(f"\n[bold]Now following: {most_recent_file}[/bold]")
            console.print(t("logs_exit_hint"))
            try:
                import subprocess
                cmd = platform_compat.get_follow_logs_command(Path(most_recent_file), lines)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in process.stdout:
                    print(f"[{os.path.basename(most_recent_file)}] {line}", end='')
            except KeyboardInterrupt:
                console.print(t("logs_stopped"))
            except Exception as e:
                console.print(t("logs_error", error=str(e)))
    else:
        # Non-follow mode - show recent lines from all files
        if len(existing_log_files) == 1:
            # Single file
            log_path = existing_log_files[0]
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    for line in all_lines[-lines:]:
                        print(line, end='')
            except Exception as e:
                console.print(t("logs_error", error=str(e)))
        else:
            # Multiple files - show recent lines from each file
            lines_per_file = lines // len(existing_log_files)
            if lines_per_file == 0:
                lines_per_file = 1
                
            for log_path in existing_log_files:
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        file_lines = f.readlines()
                        console.print(f"\n[bold]=== {os.path.basename(log_path)} ===[/bold]")
                        for line in file_lines[-lines_per_file:]:
                            print(line, end='')
                except Exception as e:
                    console.print(t("logs_error", error=str(e)))

@cli.command(help=t("search_desc"))
@click.argument('query')
@click.option('--top-k', type=int)
@click.option('--threshold', type=float)
@click.option('--explain', is_flag=True)
def search(query, top_k, threshold, explain):
    import json
    import socket
    from core.utils.process import get_process_status, WATCHER_PID_FILE, start_background_process
    
    # Try to use Watcher's internal RPC to avoid model reload delay
    status, pid = get_process_status(WATCHER_PID_FILE)
    results = None
    proxy_success = False
    
    # RPC Port (should match core.watcher.RPC_PORT)
    RPC_PORT = 11405
    
    if status == "running":
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5.0)
                s.connect(('127.0.0.1', RPC_PORT))
                
                req_data = json.dumps({
                    "action": "search",
                    "query": query,
                    "top_k": top_k,
                    "threshold": threshold,
                    "explain": explain
                })
                s.sendall(req_data.encode('utf-8'))
                
                # Receive response
                response_chunks = []
                while True:
                    chunk = s.recv(4096)
                    if not chunk: break
                    response_chunks.append(chunk)
                
                full_response = b"".join(response_chunks).decode('utf-8')
                if full_response:
                    resp_data = json.loads(full_response)
                    if resp_data.get("status") == "success":
                        results = resp_data.get('results', [])
                        proxy_success = True
        except Exception as e:
            logger.debug(f"Watcher RPC Search failed, falling back to local: {e}")

    if not proxy_success:
        # Fallback to local search
        from core.factories import initialize_system
        context_manager = initialize_system()
        results = context_manager.recursive_retrieve(
            query=query, 
            top_k=top_k, 
            min_similarity=threshold,
            explain=explain
        )
        
        # If watcher wasn't running, start it in background to cache model for next time
        if status != "running":
            logger.debug("Starting background Watcher for model caching...")
            cmd = [sys.executable, os.path.abspath(__file__), "start", "--foreground"]
            start_background_process(cmd, WATCHER_PID_FILE, "cbridge-watcher.log")
    
    if not results:
        console.print(t("search_empty"))
        return
        
    # Print results count
    console.print(t("search_results_title", count=len(results), query=query))

    from core.utils.path_resolver import PathResolver
    resolver = PathResolver({'watch_dirs': get_watch_dirs(), 'parsed_docs_dir': PARSED_DOCS_DIR})
    
    for idx, res in enumerate(results, 1):
        source = res.get('uri', 'Unknown')
        score = res.get('score', 0.0)
        
        # Color code the score
        score_color = "green" if score > 0.7 else "yellow" if score > 0.4 else "red"
        
        # Resolve full path for display
        full_path = ""
        try:
            full_path = resolver.resolve_path(res.get('filename', ''), source)
        except: pass

        # 1. Header with Source and Score
        header_text = Text()
        header_text.append(f"#{idx} ", style="bold cyan")
        header_text.append(source, style="bold")
        
        # 2. Content elements
        content = []
        
        if full_path:
            content.append(Text.assemble(("  📂 Path: ", "dim"), (full_path, "dim italic underline")))

        # Match details if explain mode
        if explain and 'score_breakdown' in res:
            b = res['score_breakdown']
            stats_table = Table.grid(padding=(0, 2))
            stats_table.add_column(style="magenta")
            stats_table.add_column(style="bold")
            
            stats_table.add_row("  📊 Match Details:", "")
            stats_table.add_row("      • Semantic", f"{b.get('semantic',0):.2f}")
            if b.get('bm25', 0) > 0: stats_table.add_row("      • BM25", f"{b.get('bm25',0):.2f}")
            if b.get('keyword', 0) > 0: stats_table.add_row("      • Keyword", f"{b.get('keyword',0):.2f}")
            if b.get('title', 0) > 0: stats_table.add_row("      • Title", f"{b.get('title',0):.2f}")
            
            content.append(stats_table)
            
            if 'matched_keywords' in res and res['matched_keywords']:
                kw_str = ", ".join(res['matched_keywords'].keys())
                content.append(Text.assemble(("   🔑 Keywords: ", "yellow"), (kw_str, "default")))
        
        # Abstract
        abstract = res.get('abstract', '')
        if abstract:
            abstract_lines = abstract.strip().split('\n')
            abstract_group = []
            for line in abstract_lines:
                # Distinguish labels from content if possible
                if ": " in line:
                    label, val = line.split(": ", 1)
                    abstract_group.append(Text.assemble((f"  {label}: ", "bold cyan"), (val, "default")))
                else:
                    abstract_group.append(Text(f"     {line}"))
            content.extend(abstract_group)
        
        # Excerpts
        excerpts = res.get('relevant_excerpts', [])[:2]
        if excerpts:
            content.append(Text("\n  📝 Excerpts:", style="bold blue focus"))
            for ex in excerpts:
                clean_ex = ex.strip().replace('\n', ' ')
                if len(clean_ex) > 250:
                    clean_ex = clean_ex[:247] + "..."
                content.append(Text(f"      • {clean_ex}", style="dim"))

        # Build and print Panel
        panel = Panel(
            Group(*content),
            title=header_text,
            title_align="left",
            subtitle=Text(f" Score: {score:.2f} ", style=f"bold {score_color} reverse"),
            subtitle_align="right",
            box=ROUNDED,
            border_style="bright_blue" if idx == 1 else "blue",
            expand=True
        )
        console.print(panel)
        console.print()

@cli.group(help="Manage search configuration")
def search_config():
    """Admin tools for search index"""
    pass

@cli.command(help=t("mcp_desc"))
@click.option('--port', default=11401, type=int)
def mcp(port):
    """Start MCP Server for Claude"""
    console.print(t("mcp_start"))
    start_mcp_server(port)

@cli.command(help=t("lang_desc"))
@click.argument('lang', type=click.Choice(['zh', 'en']))
def lang(lang):
    """Switch language"""
    set_language(lang)
    CONFIG["language"] = lang
    save_config(CONFIG)
    console.print(t("lang_success", lang=lang))

@cli.command(help=t("update_desc"))
def update():
    """Update ContextBridge via pip"""
    console.print(t("update_start"))
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "context-bridge"])
        console.print(t("update_success"))
    except Exception as e:
        console.print(t("update_failed", error=str(e)))

if __name__ == "__main__":
    cli()

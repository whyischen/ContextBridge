import os
import sys
import signal
import subprocess
from pathlib import Path
from typing import List, Optional
from core.utils.logger import setup_logger
from core.i18n import t

def is_process_running(pid: int) -> bool:
    """Check if a process with given PID is running."""
    if pid <= 0:
        return False
        
    if sys.platform == "win32":
        try:
            # Use tasklist with specific PID filter
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                # tasklist returns "INFO: No tasks are running..." when process not found
                if output and "INFO:" not in output and str(pid) in output:
                    return True
            return False
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False

def get_pid_from_file(pid_file: Path) -> Optional[int]:
    """Read PID from file and return it if file exists and content is valid."""
    if pid_file.exists():
        try:
            pid_str = pid_file.read_text().strip()
            if pid_str:
                return int(pid_str)
        except (ValueError, OSError):
            pass
    return None

def stop_process_by_file(pid_file: Path) -> bool:
    """Stop a process identified by its PID file and remove the file."""
    pid = get_pid_from_file(pid_file)
    if pid is None:
        if pid_file.exists():
            pid_file.unlink()
        return False
        
    success = False
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True, capture_output=True)
            success = True
        else:
            os.kill(pid, signal.SIGTERM)
            success = True
    except (ProcessLookupError, subprocess.CalledProcessError):
        # Process not found, which is fine
        success = True
    except Exception:
        success = False
    
    if pid_file.exists():
        try:
            pid_file.unlink()
        except OSError:
            pass
            
    return success

def start_background_process(cmd: List[str], pid_file: Path, log_file: Optional[Path] = None):
    """Start a background process and record its PID."""
    pid_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Ensure any existing process is stopped
    stop_process_by_file(pid_file)
    
    if sys.platform == "win32":
        # Windows: detached process
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        
        # Determine stdout/stderr
        out_stream = subprocess.DEVNULL
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            out_stream = open(log_file, "a", encoding="utf-8")
            
        proc = subprocess.Popen(
            cmd,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
            close_fds=False if log_file else True,
            stdout=out_stream,
            stderr=out_stream,
        )
        pid_file.write_text(str(proc.pid))
        return proc.pid
    else:
        # Unix: double-fork daemonize
        pid = os.fork()
        if pid > 0:
            # Parent process returns child PID
            pid_file.write_text(str(pid))
            return pid
            
        # Child process (daemon)
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        # Second fork could go here for full daemonization, but this is usually enough for CLI
        
        # Redirect output
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            logger_name = log_file.stem
            logger = setup_logger(logger_name)
            
            class LoggerWriter:
                def __init__(self, log_func):
                    self.log_func = log_func
                def write(self, msg):
                    if msg and msg.strip():
                        self.log_func(msg.strip())
                def flush(self): pass
                def isatty(self): return False
            
            sys.stdout = LoggerWriter(logger.info)
            sys.stderr = LoggerWriter(logger.error)
            
        # Execute the command or continue in the child
        # Note: In our use case, we usually call this function and then the child continues
        # to run the actual service logic (like watcher or api server).
        return 0

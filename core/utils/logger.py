import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def setup_logger(name="cbridge", log_dir=None):
    """
    Setup logger with daily rotation and compression.
    
    Args:
        name: Logger name
        log_dir: Log directory path, defaults to ~/.cbridge/logs
        
    Returns:
        Logger instance
    """
    if log_dir is None:
        log_dir = Path.home() / ".cbridge" / "logs"
    else:
        log_dir = Path(log_dir)
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Daily rotating file handler with compression
    log_file = log_dir / f"{name}.log"
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(log_file),
        when="midnight",
        interval=1,
        backupCount=30,  # Keep 30 days of logs
        encoding="utf-8"
    )
    
    # Compress rotated files
    def namer(name):
        return name + ".gz"
    
    def rotator(source, dest):
        import gzip
        import shutil
        with open(source, "rb") as f_in:
            with gzip.open(dest, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        Path(source).unlink()
    
    handler.namer = namer
    handler.rotator = rotator
    
    # Formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

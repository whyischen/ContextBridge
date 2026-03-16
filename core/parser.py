#!/usr/bin/env python3
"""
Document Parser for ContextBridge

Supports:
- Text files (.md, .txt): Direct read
- Office files (.docx, .xlsx, .pptx): MarkItDown conversion
- PDF files (.pdf): MarkItDown with optional OCR support
"""

from markitdown import MarkItDown
from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global MarkItDown instance for reuse (avoids re-initialization overhead)
_markitdown_instance = None

def get_markitdown() -> MarkItDown:
    """Get or create MarkItDown instance (singleton pattern)"""
    global _markitdown_instance
    if _markitdown_instance is None:
        _markitdown_instance = MarkItDown()
    return _markitdown_instance

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.txt': 'text',
    '.md': 'text',
    '.docx': 'office',
    '.xlsx': 'office',
    '.pptx': 'office',
    '.pdf': 'pdf',
}

def check_file_access(file_path: Path) -> tuple[bool, str]:
    """
    Check if file is accessible
    
    Returns:
        (is_accessible, error_message)
    """
    if not file_path.exists():
        return False, f"File not found: {file_path}"
    
    if not file_path.is_file():
        return False, f"Not a file: {file_path}"
    
    if not os.access(file_path, os.R_OK):
        return False, f"No read permission: {file_path}"
    
    # Check file size (limit to 100MB)
    max_size = 100 * 1024 * 1024  # 100MB
    file_size = file_path.stat().st_size
    if file_size > max_size:
        return False, f"File too large ({file_size / 1024 / 1024:.1f}MB > {max_size / 1024 / 1024:.0f}MB limit)"
    
    return True, ""

def parse_text_file(file_path: Path) -> str:
    """Parse plain text files (.txt, .md)"""
    logger.info(f"Reading text file: {file_path}")
    try:
        # Try UTF-8 first, fallback to other encodings
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        for encoding in encodings:
            try:
                content = file_path.read_text(encoding=encoding)
                logger.debug(f"Successfully read {file_path} with {encoding} encoding")
                return content
            except UnicodeDecodeError:
                continue
        
        logger.error(f"Failed to decode {file_path} with common encodings")
        return ""
    except PermissionError as e:
        logger.error(f"Permission denied reading {file_path}: {e}")
        return ""
    except Exception as e:
        logger.error(f"Failed to read text file {file_path}: {e}")
        return ""

def parse_office_file(file_path: Path, md: MarkItDown) -> str:
    """Parse Office files (.docx, .xlsx, .pptx)"""
    logger.info(f"Parsing Office document: {file_path}")
    try:
        result = md.convert(str(file_path))
        content = result.text_content or ""
        
        if not content:
            logger.warning(f"Office file {file_path} returned empty content")
        
        return content
    except PermissionError as e:
        logger.error(f"Permission denied reading {file_path}: {e}")
        return ""
    except Exception as e:
        logger.error(f"Failed to parse Office file {file_path}: {e}")
        return ""

def parse_pdf_file(file_path: Path, md: MarkItDown, use_ocr: bool = True) -> str:
    """
    Parse PDF files with optional OCR support
    
    Args:
        file_path: Path to PDF file
        md: MarkItDown instance
        use_ocr: Enable OCR for scanned PDFs (default: True)
    
    Returns:
        Extracted text content
    """
    logger.info(f"Parsing PDF: {file_path} (OCR: {use_ocr})")
    try:
        # MarkItDown handles both text-based and image-based PDFs
        # OCR is automatically applied when needed if dependencies are available
        result = md.convert(str(file_path), use_ocr=use_ocr)
        content = result.text_content or ""
        
        if not content:
            logger.warning(f"PDF {file_path} returned empty content, may be image-only without OCR")
        
        return content
    except PermissionError as e:
        logger.error(f"Permission denied reading {file_path}: {e}")
        return ""
    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {e}")
        return ""

def parse_document(file_path: Path, use_ocr: bool = True) -> str:
    """
    Parse document based on file type
    
    Args:
        file_path: Path to the file
        use_ocr: Enable OCR for PDF files (default: True)
    
    Returns:
        Extracted text content as markdown
    """
    # Check file accessibility
    is_accessible, error_msg = check_file_access(file_path)
    if not is_accessible:
        logger.error(error_msg)
        return ""
    
    suffix = file_path.suffix.lower()
    
    if suffix not in SUPPORTED_EXTENSIONS:
        logger.warning(f"Unsupported file type: {suffix}")
        return ""
    
    file_type = SUPPORTED_EXTENSIONS[suffix]
    
    try:
        # Reuse MarkItDown instance for better performance
        md = get_markitdown()
        
        if file_type == 'text':
            return parse_text_file(file_path)
        elif file_type == 'office':
            return parse_office_file(file_path, md)
        elif file_type == 'pdf':
            return parse_pdf_file(file_path, md, use_ocr=use_ocr)
        else:
            logger.error(f"Unknown file type: {file_type}")
            return ""
    except Exception as e:
        logger.error(f"Unexpected error parsing {file_path}: {e}")
        return ""

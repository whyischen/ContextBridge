from pathlib import Path
from typing import Set
import logging
from core.interfaces.parser import BaseParser

logger = logging.getLogger(__name__)

class MarkItDownParser(BaseParser):
    """Implementation of BaseParser using Microsoft's MarkItDown."""

    def __init__(self):
        self._md = None  # Lazy initialization
        self._supported_extensions = {
            '.txt', '.md', '.docx', '.xlsx', '.pptx', '.pdf'
        }

    def _ensure_initialized(self):
        """Lazy initialize MarkItDown instance on first use."""
        if self._md is None:
            try:
                from markitdown import MarkItDown
                self._md = MarkItDown()
            except ImportError as e:
                raise ImportError(f"MarkItDown not installed: {e}. Please run: pip install markitdown")

    def get_supported_extensions(self) -> Set[str]:
        return self._supported_extensions

    def parse(self, file_path: Path, **kwargs) -> str:
        """Parse document using MarkItDown."""
        use_ocr = kwargs.get('use_ocr', True)
        suffix = file_path.suffix.lower()

        self._ensure_initialized()

        try:
            if suffix in ['.txt', '.md']:
                return self._parse_text(file_path)

            # For Office and PDF, use MarkItDown's convert
            result = self._md.convert(str(file_path), use_ocr=use_ocr if suffix == '.pdf' else False)
            return result.text_content or ""

        except Exception as e:
            # 减少日志噪音，只记录非依赖问题的错误
            if "MissingDependencyException" not in str(e):
                logger.error(f"MarkItDown failed to parse {file_path}: {e}")
            raise

    def _parse_text(self, file_path: Path) -> str:
        """Helper to parse plain text files with encoding detection."""
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        for encoding in encodings:
            try:
                return file_path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        return ""

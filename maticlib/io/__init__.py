from .base import BaseLoader
from .file import TextLoader, PDFLoader, DOCXLoader
from .web import WebPageLoader

__all__ = [
    "BaseLoader",
    "TextLoader",
    "PDFLoader",
    "DOCXLoader",
    "WebPageLoader",
]

from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.core.text.chunkers.base import BaseChunker

class BaseLoader(ABC):
    def __init__(self, chunker: Optional[BaseChunker] = None):
        """
        Initialize the loader.

        Args:
            chunker: An optional chunker to split the loaded documents into segments.
                     If not provided, the entire document is yielded as a single segment.
        """
        self.chunker = chunker

    @abstractmethod
    def load(self, source: str, metadata: Optional[Dict[str, Any]] = None) -> Iterable[TextSegment]:
        """
        Load a document from the given source (file path, URL, etc.)
        and yield TextSegments.
        """
        pass

    # Basic implementation of async load, subclasses can override for true async I/O
    async def load_async(self, source: str, metadata: Optional[Dict[str, Any]] = None) -> Iterable[TextSegment]:
        """
        Load a document asynchronously.
        """
        import asyncio
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: list(self.load(source, metadata)))

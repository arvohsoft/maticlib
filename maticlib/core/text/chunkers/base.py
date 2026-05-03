from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from maticlib.core.text.models import TextSegment

class BaseChunker(ABC):
    """Abstract base class for all text chunkers."""

    def __init__(self, target_size: int = 1000, overlap_size: int = 200):
        """
        Initializes the BaseChunker.

        Args:
            target_size: Maximum character length of a single chunk.
            overlap_size: Number of characters from the previous chunk to overlap.
        """
        self.target_size = target_size
        self.overlap_size = overlap_size

    @abstractmethod
    def chunk_text(
        self,
        text: str,
        base_metadata: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> List[TextSegment]:
        """
        Split a single text string into multiple TextSegments.

        Args:
            text: The raw text content to split.
            base_metadata: Optional metadata dict to attach to each segment.
            parent_id: Optional parent segment ID for hierarchical chunking.

        Returns:
            A list of TextSegment objects.
        """
        pass

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[TextSegment]:
        """
        Accepts a list of document dictionaries and chunks each one.

        Args:
            documents: List of dicts with ``content`` (str) and ``metadata`` (dict) keys.

        Returns:
            A flat list of TextSegments from all documents.
        """
        segments = []
        for doc in documents:
            content = doc.get("content", "")
            meta = doc.get("metadata", {})
            segments.extend(self.chunk_text(content, base_metadata=meta))
        return segments

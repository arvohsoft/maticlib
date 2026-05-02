from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from maticlib.core.text.models import TextSegment

class BaseChunker(ABC):
    def __init__(self, target_size: int = 1000, overlap_size: int = 200):
        self.target_size = target_size
        self.overlap_size = overlap_size

    @abstractmethod
    def chunk_text(
        self,
        text: str,
        base_metadata: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> List[TextSegment]:
        """Split a single text string into multiple TextSegments."""
        pass

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[TextSegment]:
        """Accepts a list of dictionaries containing {"content": str, "metadata": dict}."""
        segments = []
        for doc in documents:
            content = doc.get("content", "")
            meta = doc.get("metadata", {})
            segments.extend(self.chunk_text(content, base_metadata=meta))
        return segments

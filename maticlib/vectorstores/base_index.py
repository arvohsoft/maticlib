from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings

class BaseVectorIndex(ABC):
    def __init__(self, embeddings: BaseEmbeddings):
        self.embeddings = embeddings

    @abstractmethod
    def add_segments(self, segments: List[TextSegment]) -> None:
        """Add a list of text segments to the index."""
        pass

    @abstractmethod
    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        """Search the index for the top k most similar segments to the query."""
        pass

    @abstractmethod
    def delete(self, segment_ids: List[str]) -> None:
        """Delete segments from the index by their IDs."""
        pass

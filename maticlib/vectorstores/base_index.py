from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings


class BaseVectorIndex(ABC):
    """Abstract base class for all vector store index backends."""

    def __init__(self, embeddings: BaseEmbeddings):
        """
        Initializes the BaseVectorIndex.

        Args:
            embeddings: An embeddings provider matching BaseEmbeddings.
        """
        self.embeddings = embeddings

    @abstractmethod
    def add_segments(self, segments: List[TextSegment]) -> None:
        """
        Add a list of text segments to the index.

        Args:
            segments: TextSegments to embed and store.
        """
        pass

    @abstractmethod
    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        """
        Search the index for the top k most similar segments to the query.

        Args:
            query: The natural language search query string.
            k: Number of results to return.
            filter_dict: Optional metadata key/value filters.

        Returns:
            A list of matching TextSegments.
        """
        pass

    @abstractmethod
    def delete(self, segment_ids: List[str]) -> None:
        """
        Delete segments from the index by their IDs.

        Args:
            segment_ids: List of segment ID strings to remove.
        """
        pass

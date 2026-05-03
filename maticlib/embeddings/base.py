from abc import ABC, abstractmethod
from typing import List
from maticlib.embeddings.models import EmbedQueryResponse, EmbedDocumentsResponse


class BaseEmbeddings(ABC):
    """Abstract base class for all embedding models."""

    @abstractmethod
    def embed_query(self, text: str) -> EmbedQueryResponse:
        """
        Generates an embedding for a single query string.

        Args:
            text: The text to embed.

        Returns:
            An EmbedQueryResponse containing the vector and usage metadata.
        """
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> EmbedDocumentsResponse:
        """
        Generates embeddings for a list of document strings.

        Args:
            texts: A list of texts to embed.

        Returns:
            An EmbedDocumentsResponse containing the list of vectors and usage metadata.
        """
        pass

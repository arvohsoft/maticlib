from abc import ABC, abstractmethod
from typing import List

class BaseEmbeddings(ABC):
    """Abstract base class for all embedding models."""

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """
        Generates an embedding for a single query string.
        
        Args:
            text: The text to embed.
            
        Returns:
            A list of floats representing the embedding.
        """
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of document strings.
        
        Args:
            texts: A list of texts to embed.
            
        Returns:
            A list of lists of floats representing the embeddings.
        """
        pass

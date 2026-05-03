__version__ = "0.2.2"

from maticlib.embeddings import (
    OpenAIEmbeddings,
    GoogleGenAIEmbeddings,
    MistralEmbeddings,
)

__all__ = [
    "OpenAIEmbeddings",
    "GoogleGenAIEmbeddings",
    "MistralEmbeddings",
]

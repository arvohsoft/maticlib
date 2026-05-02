from .config import VectorIndexConfig, IndexingStrategy
from .base_index import BaseVectorIndex
from .in_memory import InMemoryVectorIndex

# Optional imports handled gracefully
try:
    from .chroma import ChromaVectorIndex
except ImportError:
    pass

try:
    from .milvus import MilvusVectorIndex
except ImportError:
    pass

try:
    from .pinecone import PineconeVectorIndex
except ImportError:
    pass

try:
    from .qdrant import QdrantVectorIndex
except ImportError:
    pass

__all__ = [
    "VectorIndexConfig",
    "IndexingStrategy",
    "BaseVectorIndex",
    "InMemoryVectorIndex",
    "ChromaVectorIndex",
    "MilvusVectorIndex",
    "PineconeVectorIndex",
    "QdrantVectorIndex",
]

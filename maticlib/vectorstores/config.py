from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, model_validator
import logging

class IndexingStrategy(str, Enum):
    FLAT = "flat"    # exact search — perfect recall, slow at scale
    HNSW = "hnsw"   # approximate, fast, strong recall — recommended default
    IVF  = "ivf"    # inverted file — large collections
    LSH  = "lsh"    # locality-sensitive hashing — fastest, lowest recall

class VectorIndexConfig(BaseModel):
    # --- Beginner mode ---
    performance_profile: Optional[Literal["fast", "balanced", "accurate"]] = None
    # "fast"     → strategy=HNSW, hnsw_m=8,  ef=100, distance=cosine
    # "balanced" → strategy=HNSW, hnsw_m=16, ef=200, distance=cosine  (default)
    # "accurate" → strategy=FLAT, distance=cosine

    # --- Expert mode ---
    strategy: Optional[IndexingStrategy] = None
    # When strategy is set it overrides performance_profile entirely.
    # If both are set, emit logging.warning and use strategy.

    # HNSW parameters
    hnsw_m: int = 16
    hnsw_ef_construction: int = 200
    hnsw_ef_search: int = 50

    # IVF parameters
    ivf_nlist: int = 100
    ivf_nprobe: int = 10

    # LSH parameters
    lsh_num_bits: int = 8

    # General
    distance_metric: Literal["cosine", "l2", "dot"] = "cosine"
    collection_name: str = "maticlib"
    embedding_dimension: Optional[int] = None   # auto-detected from first embed call

    # Backend-specific
    chroma_persist_directory: Optional[str] = None   # None = in-memory
    milvus_uri: str = "http://localhost:19530"
    pinecone_index_name: Optional[str] = None
    pinecone_environment: Optional[str] = None
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None

    @model_validator(mode="after")
    def resolve_strategy(self) -> "VectorIndexConfig":
        """Apply performance_profile defaults when strategy is not explicitly set."""
        if self.strategy is not None and self.performance_profile is not None:
            logging.warning(
                "VectorIndexConfig: both strategy and performance_profile provided. "
                "strategy takes precedence."
            )
        
        if self.strategy is None:
            profile = self.performance_profile or "balanced"
            if profile == "fast":
                self.strategy = IndexingStrategy.HNSW
                self.hnsw_m = 8
                self.hnsw_ef_construction = 100
            elif profile == "accurate":
                self.strategy = IndexingStrategy.FLAT
            else:  # balanced
                self.strategy = IndexingStrategy.HNSW
                self.hnsw_m = 16
                self.hnsw_ef_construction = 200
        return self

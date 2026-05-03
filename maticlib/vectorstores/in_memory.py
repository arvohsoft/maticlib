import math
from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.exceptions import MissingDependencyError

class InMemoryVectorIndex(BaseVectorIndex):
    """
    Pure in-memory vector index using Numpy cosine similarity.

    Suitable for rapid prototyping and small-scale workloads. Requires ``numpy``.
    """

    def __init__(self, embeddings: BaseEmbeddings):
        """
        Initializes the InMemoryVectorIndex.

        Args:
            embeddings: An embeddings provider matching BaseEmbeddings.

        Raises:
            MissingDependencyError: If numpy is not installed.
        """
        super().__init__(embeddings)
        self.segments: List[TextSegment] = []
        self.vectors: List[List[float]] = []

        try:
            import numpy as np
        except ImportError as e:
            raise MissingDependencyError(
                "numpy is required for InMemoryVectorIndex. Install it with: pip install maticlib[rag]"
            ) from e

    def add_segments(self, segments: List[TextSegment]) -> None:
        if not segments:
            return
            
        texts = [s.content for s in segments]
        response = self.embeddings.embed_documents(texts)
        
        self.segments.extend(segments)
        self.vectors.extend(response.vectors)

    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        if not self.segments:
            return []

        import numpy as np

        query_res = self.embeddings.embed_query(query)
        q_vec = np.array(query_res.vector)
        
        doc_vecs = np.array(self.vectors)

        # Cosine similarity
        q_norm = np.linalg.norm(q_vec)
        d_norms = np.linalg.norm(doc_vecs, axis=1)
        
        # Avoid division by zero
        q_norm = q_norm if q_norm != 0 else 1.0
        d_norms = np.where(d_norms == 0, 1.0, d_norms)

        similarities = np.dot(doc_vecs, q_vec) / (d_norms * q_norm)
        
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_k_indices:
            seg = self.segments[idx]
            
            # Simple exact-match filter logic for in-memory
            if filter_dict:
                match = all(seg.metadata.get(key) == val for key, val in filter_dict.items())
                if not match:
                    continue
            
            results.append(seg)
            if len(results) == k:
                break
                
        return results

    def delete(self, segment_ids: List[str]) -> None:
        ids_to_remove = set(segment_ids)
        new_segments = []
        new_vectors = []
        
        for i, seg in enumerate(self.segments):
            if seg.segment_id not in ids_to_remove:
                new_segments.append(seg)
                new_vectors.append(self.vectors[i])
                
        self.segments = new_segments
        self.vectors = new_vectors

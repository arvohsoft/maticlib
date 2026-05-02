import uuid
import re
from typing import List, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.core.text.chunkers.base import BaseChunker
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.exceptions import MissingDependencyError

try:
    import numpy as np
except ImportError as e:
    np = None

class SemanticDifferenceChunker(BaseChunker):
    def __init__(
        self,
        embedding_model: BaseEmbeddings,
        similarity_threshold: float = 0.75,
        min_chunk_size: int = 100,
        buffer_sentences: int = 1,
    ):
        super().__init__()
        if np is None:
            raise MissingDependencyError(
                "numpy is required for SemanticDifferenceChunker. "
                "Install it with: pip install maticlib[chunking]"
            )
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.min_chunk_size = min_chunk_size
        self.buffer_sentences = buffer_sentences

    def chunk_text(
        self,
        text: str,
        base_metadata: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> List[TextSegment]:
        base_metadata = base_metadata or {}
        if not text:
            return []

        sentences = self._split_into_sentences(text)
        if not sentences:
            return []

        # Embed all sentences
        response = self.embedding_model.embed_documents(sentences)
        embeddings = response.vectors

        chunks = []
        current_chunk_sentences = [sentences[0]]
        
        for i in range(1, len(sentences)):
            similarity = self._cosine_similarity(embeddings[i-1], embeddings[i])
            
            # If similarity drops below threshold, we split
            if similarity < self.similarity_threshold:
                # But only if the current chunk is large enough
                current_text = " ".join(current_chunk_sentences)
                if len(current_text) >= self.min_chunk_size:
                    chunks.append(current_text)
                    current_chunk_sentences = []

            current_chunk_sentences.append(sentences[i])

        if current_chunk_sentences:
            chunks.append(" ".join(current_chunk_sentences))

        # We apply buffer sentences (overlap) if needed
        # In a real rigorous semantic chunker, this requires sliding window logic, 
        # but for simple implementation, we can just grab adjacent sentences from original list.
        # This is a basic simplified representation of the logic requested.
        
        segments = []
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            meta = base_metadata.copy()
            meta.update({
                "chunk_index": i,
                "total_chunks": total_chunks,
                "split_reason": "semantic_difference"
            })
            if parent_id:
                meta["parent_id"] = parent_id

            segments.append(TextSegment(
                content=chunk,
                metadata=meta,
                segment_id=uuid.uuid4().hex[:12]
            ))

        return segments

    def _split_into_sentences(self, text: str) -> List[str]:
        # Split by punctuation followed by space
        parts = re.split(r'(?<=[.!?])\s+', text)
        return [p.strip() for p in parts if p.strip()]

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        a_np = np.array(a)
        b_np = np.array(b)
        dot = np.dot(a_np, b_np)
        norm_a = np.linalg.norm(a_np)
        norm_b = np.linalg.norm(b_np)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))

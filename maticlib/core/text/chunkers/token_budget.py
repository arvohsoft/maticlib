import uuid
from typing import List, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.core.text.chunkers.base import BaseChunker
from maticlib.exceptions import MissingDependencyError


class TokenBudgetChunker(BaseChunker):
    def __init__(
        self,
        target_tokens: int = 256,
        overlap_tokens: int = 32,
        tokeniser: Optional[Any] = None,
    ):
        super().__init__(target_size=target_tokens, overlap_size=overlap_tokens)
        self.tokeniser = tokeniser

        # Check if they are trying to use tiktoken explicitly
        if self.tokeniser and getattr(self.tokeniser, "__module__", "").startswith(
            "tiktoken"
        ):
            try:
                import tiktoken
            except ImportError as e:
                raise MissingDependencyError(
                    "tiktoken is required for TokenBudgetChunker when using a tiktoken encoding. "
                    "Install it with: pip install maticlib[chunking]"
                ) from e

    def chunk_text(
        self,
        text: str,
        base_metadata: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> List[TextSegment]:
        base_metadata = base_metadata or {}
        if not text:
            return []

        # Simple split by space to chunk words, then aggregate by tokens
        words = text.split(" ")
        chunks = []
        current_chunk = []
        current_tokens = 0

        for word in words:
            word_with_space = word + " "
            word_tokens = self._count_tokens(word_with_space)

            if current_tokens + word_tokens > self.target_size and current_chunk:
                chunks.append("".join(current_chunk).strip())

                # Overlap logic
                overlap_chunk = []
                overlap_tokens = 0
                for item in reversed(current_chunk):
                    item_tokens = self._count_tokens(item)
                    if overlap_tokens + item_tokens <= self.overlap_size:
                        overlap_chunk.insert(0, item)
                        overlap_tokens += item_tokens
                    else:
                        break

                current_chunk = overlap_chunk
                current_tokens = overlap_tokens

            current_chunk.append(word_with_space)
            current_tokens += word_tokens

        if current_chunk:
            chunks.append("".join(current_chunk).strip())

        segments = []
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            meta = base_metadata.copy()
            meta.update(
                {
                    "chunk_index": i,
                    "total_chunks": total_chunks,
                    "estimated_tokens": self._count_tokens(chunk),
                }
            )
            if parent_id:
                meta["parent_id"] = parent_id

            segments.append(
                TextSegment(
                    content=chunk, metadata=meta, segment_id=uuid.uuid4().hex[:12]
                )
            )

        return segments

    def _count_tokens(self, text: str) -> int:
        if self.tokeniser:
            try:
                return len(self.tokeniser.encode(text))
            except Exception:
                pass
        return max(1, len(text) // 4)

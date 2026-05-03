import uuid
from typing import List, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.core.text.chunkers.base import BaseChunker

class SeparatorChunker(BaseChunker):
    def __init__(
        self,
        separator: str = "\n\n",
        target_size: int = 1000,
        overlap_size: int = 200,
    ):
        """
        Initializes the SeparatorChunker.

        Args:
            separator: The string used to split the text (default ``\\n\\n``).
            target_size: Maximum character length of a single chunk.
            overlap_size: Number of characters from the previous chunk to overlap.
        """
        super().__init__(target_size, overlap_size)
        self.separator = separator

    def chunk_text(
        self,
        text: str,
        base_metadata: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> List[TextSegment]:
        """
        Splits text by the separator and groups splits into chunks.

        Args:
            text: The raw text content to split.
            base_metadata: Optional metadata to attach to each segment.
            parent_id: Optional parent segment ID.

        Returns:
            A list of TextSegment objects.
        """
        base_metadata = base_metadata or {}
        if not text:
            return []

        splits = text.split(self.separator)
        chunks = []
        current_chunk = []
        current_length = 0

        for split in splits:
            split_len = len(split)
            if current_length + split_len + len(self.separator) > self.target_size and current_chunk:
                chunks.append(self.separator.join(current_chunk))
                
                # Handling overlap logic (simple implementation)
                # Keep adding from the end of current_chunk until overlap size is reached
                overlap_chunk = []
                overlap_length = 0
                for item in reversed(current_chunk):
                    if overlap_length + len(item) + len(self.separator) <= self.overlap_size:
                        overlap_chunk.insert(0, item)
                        overlap_length += len(item) + len(self.separator)
                    else:
                        break
                
                current_chunk = overlap_chunk
                current_length = overlap_length

            current_chunk.append(split)
            current_length += split_len + len(self.separator)

        if current_chunk:
            chunks.append(self.separator.join(current_chunk))

        segments = []
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            meta = base_metadata.copy()
            meta.update({
                "chunk_index": i,
                "total_chunks": total_chunks,
            })
            if parent_id:
                meta["parent_id"] = parent_id

            segments.append(TextSegment(
                content=chunk,
                metadata=meta,
                segment_id=uuid.uuid4().hex[:12]
            ))

        return segments

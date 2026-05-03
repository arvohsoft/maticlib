import uuid
from typing import List, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.core.text.chunkers.base import BaseChunker


class HierarchicalChunker(BaseChunker):
    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(
        self,
        separators: Optional[List[str]] = None,
        target_size: int = 1000,
        overlap_size: int = 200,
        language: Optional[str] = None,
    ):
        super().__init__(target_size, overlap_size)
        if language:
            self.separators = self._get_separators_for_language(language)
        else:
            self.separators = separators or self.DEFAULT_SEPARATORS

    def chunk_text(
        self,
        text: str,
        base_metadata: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> List[TextSegment]:
        base_metadata = base_metadata or {}
        if not text:
            return []

        chunks_with_seps = self._split_recursive(text, self.separators)

        segments = []
        total_chunks = len(chunks_with_seps)
        for i, (chunk, sep_used) in enumerate(chunks_with_seps):
            meta = base_metadata.copy()
            meta.update(
                {
                    "chunk_index": i,
                    "total_chunks": total_chunks,
                    "separator_used": sep_used,
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

    def _split_recursive(
        self, text: str, separators: List[str]
    ) -> List[tuple[str, str]]:
        if len(text) <= self.target_size:
            return [(text, "")]

        if not separators:
            # Fallback: slice directly if out of separators
            chunks = []
            for i in range(0, len(text), self.target_size - self.overlap_size):
                chunks.append((text[i : i + self.target_size], ""))
            return chunks

        separator = separators[0]

        if not separator:
            # Empty string separator: split character by character
            splits = list(text)
        else:
            splits = text.split(separator)

        if len(splits) == 1:
            # Separator not found, try the next one
            return self._split_recursive(text, separators[1:])

        chunks = []
        current_chunk = []
        current_length = 0

        for i, split in enumerate(splits):
            part = split if i == 0 or not separator else separator + split
            if not part:
                continue

            if len(part) > self.target_size:
                if current_chunk:
                    chunks.append(("".join(current_chunk), separator))
                    current_chunk = []
                    current_length = 0

                sub_chunks = self._split_recursive(part, separators[1:])
                chunks.extend(sub_chunks)
            else:
                if current_length + len(part) > self.target_size and current_chunk:
                    chunks.append(("".join(current_chunk), separator))
                    # Simple overlap logic
                    current_chunk = current_chunk[-1:] if current_chunk else []
                    current_length = len(current_chunk[0]) if current_chunk else 0

                current_chunk.append(part)
                current_length += len(part)

        if current_chunk:
            chunks.append(("".join(current_chunk), separator))

        return chunks

    def _get_separators_for_language(self, language: str) -> List[str]:
        if language == "code":
            return ["\nclass ", "\ndef ", "\n\n", "\n", " ", ""]
        elif language == "japanese":
            return ["\n\n", "。", "\n", " ", ""]
        elif language == "markdown":
            return ["\n## ", "\n### ", "\n\n", "\n", " ", ""]
        return self.DEFAULT_SEPARATORS

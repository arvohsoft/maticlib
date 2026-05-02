import os
import uuid
from typing import Iterable, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.io.base import BaseLoader
from maticlib.exceptions import MissingDependencyError, DocumentLoadError

class TextLoader(BaseLoader):
    def load(self, source: str, metadata: Optional[Dict[str, Any]] = None) -> Iterable[TextSegment]:
        if not os.path.exists(source):
            raise DocumentLoadError(f"File not found: {source}")
            
        base_meta = metadata or {}
        base_meta["source"] = source
        base_meta["loader"] = "TextLoader"

        try:
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise DocumentLoadError(f"Failed to read file {source}: {e}")

        if self.chunker:
            parent_id = uuid.uuid4().hex[:12]
            yield from self.chunker.chunk_text(content, base_metadata=base_meta, parent_id=parent_id)
        else:
            yield TextSegment(
                content=content,
                metadata=base_meta,
                segment_id=uuid.uuid4().hex[:12]
            )

class PDFLoader(BaseLoader):
    def load(self, source: str, metadata: Optional[Dict[str, Any]] = None) -> Iterable[TextSegment]:
        try:
            import pypdf
        except ImportError as e:
            raise MissingDependencyError(
                "pypdf is required for PDFLoader. Install it with: pip install maticlib[rag]"
            ) from e

        if not os.path.exists(source):
            raise DocumentLoadError(f"File not found: {source}")

        base_meta = metadata or {}
        base_meta["source"] = source
        base_meta["loader"] = "PDFLoader"

        try:
            with open(source, "rb") as f:
                reader = pypdf.PdfReader(f)
                content = ""
                for page in reader.pages:
                    content += page.extract_text() + "\n\n"
        except Exception as e:
            raise DocumentLoadError(f"Failed to read PDF {source}: {e}")

        if self.chunker:
            parent_id = uuid.uuid4().hex[:12]
            yield from self.chunker.chunk_text(content, base_metadata=base_meta, parent_id=parent_id)
        else:
            yield TextSegment(
                content=content,
                metadata=base_meta,
                segment_id=uuid.uuid4().hex[:12]
            )

class DOCXLoader(BaseLoader):
    def load(self, source: str, metadata: Optional[Dict[str, Any]] = None) -> Iterable[TextSegment]:
        try:
            import docx
        except ImportError as e:
            raise MissingDependencyError(
                "python-docx is required for DOCXLoader. Install it with: pip install maticlib[rag]"
            ) from e

        if not os.path.exists(source):
            raise DocumentLoadError(f"File not found: {source}")

        base_meta = metadata or {}
        base_meta["source"] = source
        base_meta["loader"] = "DOCXLoader"

        try:
            doc = docx.Document(source)
            content = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise DocumentLoadError(f"Failed to read DOCX {source}: {e}")

        if self.chunker:
            parent_id = uuid.uuid4().hex[:12]
            yield from self.chunker.chunk_text(content, base_metadata=base_meta, parent_id=parent_id)
        else:
            yield TextSegment(
                content=content,
                metadata=base_meta,
                segment_id=uuid.uuid4().hex[:12]
            )

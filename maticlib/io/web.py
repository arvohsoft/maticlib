import uuid
import httpx
from typing import Iterable, Dict, Any, Optional
from maticlib.core.text.models import TextSegment
from maticlib.io.base import BaseLoader
from maticlib.exceptions import MissingDependencyError, DocumentLoadError


class WebPageLoader(BaseLoader):
    """Fetches a URL and extracts readable text using BeautifulSoup. Requires beautifulsoup4 and httpx."""

    def load(
        self, source: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Iterable[TextSegment]:
        """
        Fetches a web page and yields TextSegments.

        Args:
            source: The URL of the page to fetch.
            metadata: Optional metadata dict to attach to each segment.

        Returns:
            An iterable of TextSegment objects with the page's cleaned text.
        """

        try:
            from bs4 import BeautifulSoup
        except ImportError as e:
            raise MissingDependencyError(
                "beautifulsoup4 is required for WebPageLoader. Install it with: pip install maticlib[rag]"
            ) from e

        base_meta = metadata or {}
        base_meta["source"] = source
        base_meta["loader"] = "WebPageLoader"

        try:
            with httpx.Client(follow_redirects=True, timeout=10.0) as client:
                response = client.get(source)
                response.raise_for_status()
                html = response.text
        except Exception as e:
            raise DocumentLoadError(f"Failed to fetch URL {source}: {e}")

        try:
            soup = BeautifulSoup(html, "html.parser")
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.extract()

            # Get text and clean up whitespace
            text = soup.get_text(separator="\n")
            lines = (line.strip() for line in text.splitlines())
            chunks_text = (line for line in lines if line)
            content = "\n".join(chunks_text)
        except Exception as e:
            raise DocumentLoadError(f"Failed to parse HTML from {source}: {e}")

        if self.chunker:
            parent_id = uuid.uuid4().hex[:12]
            yield from self.chunker.chunk_text(
                content, base_metadata=base_meta, parent_id=parent_id
            )
        else:
            yield TextSegment(
                content=content, metadata=base_meta, segment_id=uuid.uuid4().hex[:12]
            )

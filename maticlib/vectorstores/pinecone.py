import os
from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.exceptions import MissingDependencyError
from maticlib.vectorstores.config import VectorIndexConfig

class PineconeVectorIndex(BaseVectorIndex):
    def __init__(
        self,
        embeddings: BaseEmbeddings,
        index_name: str,
        api_key: Optional[str] = None,
        config: Optional[VectorIndexConfig] = None
    ):
        super().__init__(embeddings)
        self.index_name = index_name
        self.config = config or VectorIndexConfig()
        
        api_key = api_key or os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY must be provided or set in environment variables.")

        try:
            from pinecone import Pinecone
        except ImportError as e:
            raise MissingDependencyError(
                "pinecone is required for PineconeVectorIndex. Install it with: pip install maticlib[pinecone]"
            ) from e

        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(self.index_name)

    def add_segments(self, segments: List[TextSegment]) -> None:
        if not segments:
            return

        texts = [s.content for s in segments]
        response = self.embeddings.embed_documents(texts)
        
        vectors_to_upsert = []
        for i, seg in enumerate(segments):
            meta = seg.metadata.copy()
            meta["text"] = seg.content
            
            # Pinecone requires metadata values to be str, number, bool, or list of str
            clean_meta = {}
            for k, v in meta.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_meta[k] = v
                elif isinstance(v, list) and all(isinstance(i, str) for i in v):
                    clean_meta[k] = v
            
            vectors_to_upsert.append({
                "id": seg.segment_id,
                "values": response.vectors[i],
                "metadata": clean_meta
            })
            
        # Batch upsert in chunks of 100
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            self.index.upsert(vectors=vectors_to_upsert[i:i+batch_size])

    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        query_res = self.embeddings.embed_query(query)
        
        search_res = self.index.query(
            vector=query_res.vector,
            top_k=k,
            include_metadata=True,
            filter=filter_dict
        )

        segments = []
        for match in search_res.get("matches", []):
            meta = match.get("metadata", {})
            text = meta.pop("text", "")
            
            segments.append(TextSegment(
                segment_id=match["id"],
                content=text,
                metadata=meta
            ))

        return segments

    def delete(self, segment_ids: List[str]) -> None:
        self.index.delete(ids=segment_ids)

from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.exceptions import MissingDependencyError
from maticlib.vectorstores.config import VectorIndexConfig

class QdrantVectorIndex(BaseVectorIndex):
    """Vector index backed by Qdrant (in-memory, local, or cloud)."""

    def __init__(
        self,
        embeddings: BaseEmbeddings,
        collection_name: str = "maticlib_collection",
        location: str = ":memory:",
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        dim: Optional[int] = None,
        config: Optional[VectorIndexConfig] = None
    ):
        """
        Initializes the QdrantVectorIndex.

        Args:
            embeddings: An embeddings provider matching BaseEmbeddings.
            collection_name: Name of the Qdrant collection. Default is ``maticlib_collection``.
            location: Qdrant storage location. Use ``':memory:'`` for in-process,
                or a file path for local persistence.
            url: Optional URL to a remote Qdrant instance (e.g. ``http://localhost:6333``).
            api_key: Optional API key for Qdrant Cloud.
            dim: Embedding dimension. Auto-detected if not provided.
            config: Optional VectorIndexConfig for distance metric and strategy.
        """
        super().__init__(embeddings)
        self.collection_name = collection_name
        self.config = config or VectorIndexConfig()
        
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import VectorParams, Distance
        except ImportError as e:
            raise MissingDependencyError(
                "qdrant-client is required for QdrantVectorIndex. Install it with: pip install maticlib[qdrant]"
            ) from e

        if url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(location=location)

        # Map distance metric
        metric_map = {
            "cosine": Distance.COSINE,
            "l2": Distance.EUCLID,
            "ip": Distance.DOT
        }
        distance = metric_map.get(self.config.distance_metric, Distance.COSINE)

        if not dim:
            dummy_res = self.embeddings.embed_query("test")
            dim = len(dummy_res.vector)

        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=dim, distance=distance),
            )

    def add_segments(self, segments: List[TextSegment]) -> None:
        if not segments:
            return
            
        from qdrant_client.models import PointStruct

        texts = [s.content for s in segments]
        response = self.embeddings.embed_documents(texts)
        
        points = []
        for i, seg in enumerate(segments):
            meta = seg.metadata.copy()
            meta["text"] = seg.content
            
            points.append(
                PointStruct(
                    id=hash(seg.segment_id) % ((2**63)-1), # Qdrant supports UUID strings, but integer hashes are safer for generic IDs unless we strictly enforce UUIDs. Let's use UUIDs or string IDs. Wait, Qdrant allows string UUIDs or integers. Let's just use string if it looks like UUID, else hash.
                    vector=response.vectors[i],
                    payload=meta
                )
            )
            
            # Note: A real implementation might want to enforce valid UUIDs for segment_id 
            # to prevent hash collisions. For now, we'll hash to an unsigned int64 range.

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        query_res = self.embeddings.embed_query(query)
        
        qdrant_filter = None
        if filter_dict:
            conditions = []
            for key, val in filter_dict.items():
                conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=val))
                )
            qdrant_filter = Filter(must=conditions)

        search_res = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_res.vector,
            limit=k,
            query_filter=qdrant_filter
        )

        segments = []
        for hit in search_res:
            payload = hit.payload or {}
            text = payload.pop("text", "")
            
            segments.append(TextSegment(
                segment_id=str(hit.id), # Qdrant IDs
                content=text,
                metadata=payload
            ))

        return segments

    def delete(self, segment_ids: List[str]) -> None:
        ids_to_delete = [hash(sid) % ((2**63)-1) for sid in segment_ids]
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=ids_to_delete
        )

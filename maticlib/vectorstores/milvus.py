from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.exceptions import MissingDependencyError
from maticlib.vectorstores.config import VectorIndexConfig

class MilvusVectorIndex(BaseVectorIndex):
    def __init__(
        self,
        embeddings: BaseEmbeddings,
        collection_name: str = "maticlib_collection",
        uri: str = "./milvus_demo.db", # Lite mode by default
        dim: Optional[int] = None,
        config: Optional[VectorIndexConfig] = None
    ):
        super().__init__(embeddings)
        self.collection_name = collection_name
        self.config = config or VectorIndexConfig()
        
        try:
            from pymilvus import MilvusClient
        except ImportError as e:
            raise MissingDependencyError(
                "pymilvus is required for MilvusVectorIndex. Install it with: pip install maticlib[milvus]"
            ) from e

        self.client = MilvusClient(uri=uri)
        
        # If dimension is not provided, we embed a dummy text to figure it out
        if not dim:
            dummy_res = self.embeddings.embed_query("test")
            dim = len(dummy_res.vector)

        if not self.client.has_collection(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                dimension=dim,
                metric_type=self.config.distance_metric.upper() if self.config.distance_metric in ["cosine", "l2", "ip"] else "L2"
            )

    def add_segments(self, segments: List[TextSegment]) -> None:
        if not segments:
            return

        texts = [s.content for s in segments]
        response = self.embeddings.embed_documents(texts)
        
        data = []
        for i, seg in enumerate(segments):
            # We must pass the id, vector, and any metadata/content
            row = {
                "id": hash(seg.segment_id) % ((2**63)-1), # Milvus needs integer IDs by default or specified schema
                "vector": response.vectors[i],
                "text": seg.content,
                "segment_id": seg.segment_id
            }
            # Merge safe metadata
            for k, v in seg.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    row[k] = v
            data.append(row)

        self.client.insert(collection_name=self.collection_name, data=data)

    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        query_res = self.embeddings.embed_query(query)
        
        # Simple translation of dict to Milvus boolean expression
        filter_expr = ""
        if filter_dict:
            conditions = []
            for key, val in filter_dict.items():
                if isinstance(val, str):
                    conditions.append(f"{key} == '{val}'")
                else:
                    conditions.append(f"{key} == {val}")
            filter_expr = " and ".join(conditions)

        search_res = self.client.search(
            collection_name=self.collection_name,
            data=[query_res.vector],
            limit=k,
            filter=filter_expr if filter_expr else None,
            output_fields=["text", "segment_id"]
        )

        segments = []
        if not search_res:
            return segments

        for hits in search_res:
            for hit in hits:
                entity = hit.get("entity", {})
                segments.append(TextSegment(
                    segment_id=entity.get("segment_id", str(hit.get("id"))),
                    content=entity.get("text", ""),
                    metadata={k:v for k,v in entity.items() if k not in ["text", "segment_id"]}
                ))

        return segments

    def delete(self, segment_ids: List[str]) -> None:
        expr = f"segment_id in {[f'{sid}' for sid in segment_ids]}"
        self.client.delete(collection_name=self.collection_name, filter=expr)

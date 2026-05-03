from typing import List, Optional, Any, Dict
from maticlib.core.text.models import TextSegment
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.exceptions import MissingDependencyError
from maticlib.vectorstores.config import VectorIndexConfig


class ChromaVectorIndex(BaseVectorIndex):
    """Vector index backed by ChromaDB (ephemeral or persistent)."""

    def __init__(
        self,
        embeddings: BaseEmbeddings,
        collection_name: str = "maticlib_collection",
        persist_directory: Optional[str] = None,
        config: Optional[VectorIndexConfig] = None,
    ):
        """
        Initializes the ChromaVectorIndex.

        Args:
            embeddings: An embeddings provider matching BaseEmbeddings.
            collection_name: Name of the Chroma collection. Default is ``maticlib_collection``.
            persist_directory: If set, uses a PersistentClient saving to this directory.
            config: Optional VectorIndexConfig for distance metric settings.
        """
        super().__init__(embeddings)
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.config = config or VectorIndexConfig()

        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            raise MissingDependencyError(
                "chromadb is required for ChromaVectorIndex. Install it with: pip install maticlib[chroma]"
            ) from e

        if self.persist_directory:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        else:
            self.client = chromadb.EphemeralClient()

        # Chroma doesn't natively support HNSW config via standard create_collection easily without specific hnsw:space metadata
        metadata = {"hnsw:space": self.config.distance_metric}
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name, metadata=metadata
        )

    def add_segments(self, segments: List[TextSegment]) -> None:
        if not segments:
            return

        texts = [s.content for s in segments]
        response = self.embeddings.embed_documents(texts)

        ids = [s.segment_id for s in segments]
        metadatas = [s.metadata for s in segments]

        # Filter out complex metadata objects that chromadb might reject
        clean_metadatas = []
        for meta in metadatas:
            clean_meta = {
                k: v for k, v in meta.items() if isinstance(v, (str, int, float, bool))
            }
            clean_metadatas.append(clean_meta)

        self.collection.add(
            embeddings=response.vectors,
            documents=texts,
            metadatas=clean_metadatas,
            ids=ids,
        )

    def similarity_search(
        self, query: str, k: int = 4, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[TextSegment]:
        query_res = self.embeddings.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_res.vector], n_results=k, where=filter_dict
        )

        segments = []
        if not results["documents"] or not results["documents"][0]:
            return segments

        for i in range(len(results["documents"][0])):
            doc = results["documents"][0][i]
            meta = results["metadatas"][0][i] if results["metadatas"] else {}
            doc_id = results["ids"][0][i]

            segments.append(TextSegment(segment_id=doc_id, content=doc, metadata=meta))

        return segments

    def delete(self, segment_ids: List[str]) -> None:
        self.collection.delete(ids=segment_ids)

from typing import List, Optional, Dict, Any
from maticlib.core.text.models import TextSegment
from maticlib.vectorstores.base_index import BaseVectorIndex

class HybridRetriever:
    """
    Combines vector search with exact keyword matching.
    """
    def __init__(self, vector_index: BaseVectorIndex):
        """
        Initializes the HybridRetriever.

        Args:
            vector_index: A vector store index matching BaseVectorIndex.
        """
        self.vector_index = vector_index

    def retrieve(self, query: str, k: int = 4, keywords: Optional[List[str]] = None, filter_dict: Optional[Dict[str, Any]] = None) -> List[TextSegment]:
        """
        Retrieves top k segments from the vector index.

        Args:
            query: The natural language search query.
            k: Number of segments to return.
            keywords: Optional list of keywords for boosting/filtering.
            filter_dict: Optional metadata filters.

        Returns:
            A list of retrieved TextSegments.
        """
        # Over-fetch from vector store
        fetch_k = k * 2 if keywords else k
        segments = self.vector_index.similarity_search(query, k=fetch_k, filter_dict=filter_dict)
        
        if not keywords:
            return segments[:k]
            
        # Very basic hybrid scoring: keyword matching
        scored_segments = []
        for seg in segments:
            score = 0
            text_lower = seg.content.lower()
            for kw in keywords:
                if kw.lower() in text_lower:
                    score += 1
            scored_segments.append((score, seg))
            
        # Sort by keyword score descending, then return top k
        scored_segments.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored_segments][:k]

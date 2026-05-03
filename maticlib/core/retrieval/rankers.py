from typing import List
from maticlib.core.text.models import TextSegment


class ReciprocalRankFusion:
    """
    RRF algorithm to combine results from multiple searches.
    """

    def __init__(self, k: int = 60):
        self.k = k

    def rank(self, result_lists: List[List[TextSegment]]) -> List[TextSegment]:
        scores = {}
        segment_map = {}

        for results in result_lists:
            for rank, seg in enumerate(results):
                sid = seg.segment_id
                if sid not in scores:
                    scores[sid] = 0.0
                    segment_map[sid] = seg
                # RRF score formula
                scores[sid] += 1.0 / (self.k + rank + 1)

        # Sort by RRF score descending
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return [segment_map[sid] for sid in sorted_ids]

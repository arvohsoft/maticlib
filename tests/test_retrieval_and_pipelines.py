import pytest
from maticlib.core.text.models import TextSegment
from maticlib.core.retrieval.hybrid import HybridRetriever
from maticlib.core.retrieval.rankers import ReciprocalRankFusion
from maticlib.core.retrieval.transformers import QueryTransformer


class DummyIndex:
    def similarity_search(self, query, k=4, filter_dict=None):
        return [
            TextSegment(content="Apple pie recipe", segment_id="1"),
            TextSegment(content="Banana split", segment_id="2"),
            TextSegment(content="Apple juice", segment_id="3"),
        ][:k]


def test_hybrid_retrieval():
    index = DummyIndex()
    retriever = HybridRetriever(vector_index=index)

    # Keyword 'juice' should boost segment 3 to the top if we use keywords
    results = retriever.retrieve("apple", k=2, keywords=["juice"])
    assert len(results) == 2
    assert results[0].content == "Apple juice"


def test_rrf_ranker():
    ranker = ReciprocalRankFusion()

    list1 = [
        TextSegment(content="A", segment_id="1"),
        TextSegment(content="B", segment_id="2"),
    ]
    list2 = [
        TextSegment(content="C", segment_id="3"),
        TextSegment(content="A", segment_id="1"),
    ]

    results = ranker.rank([list1, list2])
    # Segment 1 is in both lists (rank 0 in list1, rank 1 in list2)
    # It should have the highest score and be first
    assert results[0].segment_id == "1"


def test_query_transformer():
    class DummyLLM:
        def complete(self, prompt):
            return "Query var 1\nQuery var 2"

        def get_text_response(self, res):
            return res

    transformer = QueryTransformer(llm_client=DummyLLM())
    vars = transformer.generate_variations("test", n=2)
    assert len(vars) == 2
    assert vars[0] == "Query var 1"

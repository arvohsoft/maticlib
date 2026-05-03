import pytest
from maticlib.core.text.models import TextSegment
from maticlib.vectorstores.in_memory import InMemoryVectorIndex
from maticlib.vectorstores.schema_index import SchemaVectorIndex
from maticlib.core.text2sql.models import TableSchema, ColumnSchema


class DummyEmbeddings:
    def embed_query(self, text):
        from maticlib.embeddings.base import EmbedQueryResponse

        return EmbedQueryResponse(vector=[0.1, 0.2, 0.3], prompt_tokens=1)

    def embed_documents(self, texts):
        from maticlib.embeddings.base import EmbedDocumentsResponse

        return EmbedDocumentsResponse(
            vectors=[[0.1, 0.2, 0.3] for _ in texts], prompt_tokens=len(texts)
        )


def test_in_memory_index():
    try:
        import numpy
    except ImportError:
        pytest.skip("numpy missing")

    embeddings = DummyEmbeddings()
    index = InMemoryVectorIndex(embeddings=embeddings)

    seg1 = TextSegment(
        content="Hello world", segment_id="1", metadata={"type": "greeting"}
    )
    seg2 = TextSegment(
        content="Goodbye world", segment_id="2", metadata={"type": "farewell"}
    )

    index.add_segments([seg1, seg2])
    assert len(index.segments) == 2

    results = index.similarity_search("hello", k=1)
    assert len(results) == 1

    results = index.similarity_search("hello", k=1, filter_dict={"type": "greeting"})
    assert len(results) == 1
    assert results[0].segment_id == "1"

    index.delete(["1"])
    assert len(index.segments) == 1


def test_schema_index():
    try:
        import numpy
    except ImportError:
        pytest.skip("numpy missing")

    embeddings = DummyEmbeddings()
    vector_index = InMemoryVectorIndex(embeddings=embeddings)
    schema_index = SchemaVectorIndex(vector_index=vector_index)

    col1 = ColumnSchema(name="id", data_type="INTEGER", primary_key=True)
    table = TableSchema(name="users", columns=[col1])

    schema_index.add_tables([table])

    # Since it's a dummy embedding (all vectors are the same), it will just return the first match
    results = schema_index.retrieve_relevant_tables("get users", k=1)
    assert len(results) == 1
    assert "CREATE TABLE users" in results[0]

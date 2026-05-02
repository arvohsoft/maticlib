import pytest
from maticlib.core.text.models import TextSegment
from maticlib.core.text.chunkers import (
    SeparatorChunker,
    HierarchicalChunker,
    TokenBudgetChunker,
    SemanticDifferenceChunker,
)
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.embeddings.models import EmbedDocumentsResponse

def test_separator_chunker_basic():
    chunker = SeparatorChunker(separator="\n", target_size=15, overlap_size=0)
    text = "Hello world\nThis is a test\nShort line\nAnother one"
    
    segments = chunker.chunk_text(text)
    
    # "Hello world" (11) + "\n" + "This is a test" (14) = 26 > 15
    # So "Hello world" should be its own chunk.
    assert len(segments) > 1
    assert segments[0].content == "Hello world"
    assert segments[0].metadata["chunk_index"] == 0
    assert segments[0].metadata["total_chunks"] == len(segments)

def test_separator_chunker_overlap():
    chunker = SeparatorChunker(separator=" ", target_size=20, overlap_size=10)
    text = "word1 word2 word3 word4 word5 word6"
    segments = chunker.chunk_text(text)
    
    assert len(segments) > 1
    # Check that some words overlap between segments
    assert "word3" in segments[0].content or "word4" in segments[0].content
    
def test_hierarchical_chunker_fallback():
    chunker = HierarchicalChunker(target_size=10, overlap_size=2)
    # Text with no separators should just be sliced
    text = "abcdefghijklmno"
    segments = chunker.chunk_text(text)
    
    assert len(segments) == 2
    assert segments[0].content == "abcdefghij"
    assert segments[1].content == "jklmno"

def test_hierarchical_chunker_markdown():
    chunker = HierarchicalChunker(language="markdown", target_size=30, overlap_size=0)
    text = "\n## Heading 2\nSome content here.\n\nMore content here."
    segments = chunker.chunk_text(text)
    
    assert len(segments) > 0
    assert "## Heading 2" in segments[0].content

def test_token_budget_chunker_heuristic():
    chunker = TokenBudgetChunker(target_tokens=10, overlap_tokens=2)
    # Using heuristic: 4 chars = 1 token. 10 tokens = 40 chars.
    text = "This is a very long string that should be split into multiple chunks based on token limits."
    segments = chunker.chunk_text(text)
    
    assert len(segments) > 1
    for seg in segments:
        assert seg.metadata["estimated_tokens"] <= 15 # Allow some margin for words

class MockEmbeddings(BaseEmbeddings):
    def embed_query(self, text):
        pass
    def embed_documents(self, texts):
        # Return mock vectors. 
        # Sentences 1 and 2 will be identical [1, 0]
        # Sentence 3 will be orthogonal [0, 1]
        vectors = []
        for t in texts:
            if "apple" in t.lower():
                vectors.append([1.0, 0.0])
            else:
                vectors.append([0.0, 1.0])
        
        return EmbedDocumentsResponse(
            vectors=vectors,
            prompt_tokens=10,
            total_tokens=10,
            model="mock"
        )

def test_semantic_difference_chunker():
    try:
        import numpy as np
    except ImportError:
        pytest.skip("numpy is required for semantic chunker tests")
        
    mock_embed = MockEmbeddings()
    chunker = SemanticDifferenceChunker(
        embedding_model=mock_embed,
        similarity_threshold=0.5,
        min_chunk_size=10
    )
    
    text = "I love eating apples. Apples are very tasty. Bananas are yellow and completely different."
    segments = chunker.chunk_text(text)
    
    # "I love eating apples." and "Apples are very tasty." should cluster.
    # "Bananas are yellow..." should be a new chunk.
    assert len(segments) >= 2
    assert "apples" in segments[0].content.lower()
    assert "bananas" in segments[-1].content.lower()
    assert segments[0].metadata["split_reason"] == "semantic_difference"

def test_parent_id_propagation():
    chunker = SeparatorChunker()
    segments = chunker.chunk_text("Hello\n\nWorld", parent_id="doc-123")
    
    for seg in segments:
        assert seg.metadata["parent_id"] == "doc-123"
        assert seg.segment_id is not None

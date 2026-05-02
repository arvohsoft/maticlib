import os
from maticlib.io.file import TextLoader
from maticlib.io.web import WebPageLoader
from maticlib.core.text.chunkers import (
    SeparatorChunker,
    HierarchicalChunker,
    TokenBudgetChunker
)

def example_text_loader_with_separator_chunker():
    print("--- 1. Separator Chunker with TextLoader ---")
    
    # Create a dummy text file
    dummy_file = "sample.txt"
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write("First paragraph.\n\nSecond paragraph.\n\nThird paragraph.")

    # Initialize a chunker that splits exactly by double newlines
    chunker = SeparatorChunker(separator="\n\n", target_size=10, overlap_size=0)
    
    # Pass the chunker directly to the loader
    loader = TextLoader(chunker=chunker)
    segments = list(loader.load(dummy_file))

    for seg in segments:
        print(f"Segment ID: {seg.segment_id}")
        print(f"Content: {seg.content}")
        print(f"Metadata: {seg.metadata}\n")
        
    os.remove(dummy_file)

def example_web_loader_with_hierarchical_chunker():
    print("--- 2. Hierarchical Chunker with WebPageLoader ---")
    
    # Load from the web and apply smart hierarchical markdown-like splitting
    chunker = HierarchicalChunker(target_size=500, overlap_size=50)
    loader = WebPageLoader(chunker=chunker)
    
    print("Fetching http://example.com ...")
    try:
        segments = list(loader.load("http://example.com"))
        print(f"Extracted {len(segments)} segments.")
        for seg in segments[:2]: # Print first 2
            print(f"Content snippet: {seg.content[:100]}...")
            print(f"Metadata: {seg.metadata}\n")
    except Exception as e:
        print(f"Skipping web load example due to error (no internet/missing deps?): {e}")

def example_token_budget_chunker():
    print("--- 3. Token Budget Chunker (Standalone) ---")
    text = "This is a long string that we want to split based on token budget. " * 10
    
    chunker = TokenBudgetChunker(target_tokens=20, overlap_tokens=5)
    segments = chunker.chunk_text(text)
    
    print(f"Split text into {len(segments)} segments using token heuristics:")
    for seg in segments[:2]:
        print(f"- {seg.content} (Tokens: {seg.metadata['estimated_tokens']})")

if __name__ == "__main__":
    example_text_loader_with_separator_chunker()
    print()
    example_web_loader_with_hierarchical_chunker()
    print()
    example_token_budget_chunker()

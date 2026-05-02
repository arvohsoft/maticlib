import os
import pytest
from maticlib.io.file import TextLoader, PDFLoader, DOCXLoader
from maticlib.io.web import WebPageLoader
from maticlib.core.text.chunkers import SeparatorChunker

def test_text_loader_no_chunker(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello\nWorld")
    
    loader = TextLoader()
    segments = list(loader.load(str(test_file)))
    
    assert len(segments) == 1
    assert segments[0].content == "Hello\nWorld"
    assert segments[0].metadata["source"] == str(test_file)

def test_text_loader_with_chunker(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello\n\nWorld")
    
    chunker = SeparatorChunker(target_size=5, overlap_size=0)
    loader = TextLoader(chunker=chunker)
    segments = list(loader.load(str(test_file)))
    
    assert len(segments) == 2
    assert segments[0].content == "Hello"
    assert segments[1].content == "World"
    assert segments[0].metadata["parent_id"] is not None

def test_pdf_loader_missing_file():
    loader = PDFLoader()
    with pytest.raises(Exception):
        list(loader.load("non_existent.pdf"))

@pytest.mark.asyncio
async def test_base_loader_async(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Async Load")
    
    loader = TextLoader()
    segments = await loader.load_async(str(test_file))
    
    assert len(segments) == 1
    assert segments[0].content == "Async Load"

def test_web_page_loader_missing_deps():
    # Will try to load without bs4 or with it, depending on env. 
    # Just checking it initializes.
    loader = WebPageLoader()
    assert loader is not None

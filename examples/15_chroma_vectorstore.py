import os
import shutil
from maticlib.embeddings.openai import OpenAIEmbeddings
from maticlib.vectorstores.chroma import ChromaVectorIndex
from maticlib.core.text.models import TextSegment

from dotenv import load_dotenv
load_dotenv()

def example_chroma_vectorstore():
    print("--- ChromaDB Vector Store Example ---")
    try:
        # Initialize Embeddings
        embeddings = OpenAIEmbeddings()
        
        # Setup Chroma persistent directory
        persist_dir = "./chroma_db_demo"
        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)
            
        print(f"Initializing ChromaVectorIndex at {persist_dir}...")
        vector_index = ChromaVectorIndex(
            embeddings=embeddings,
            collection_name="demo_collection",
            persist_directory=persist_dir
        )
        
        # Add segments
        segments = [
            TextSegment(content="Apple pie is a delicious dessert.", segment_id="apple_1", metadata={"category": "food"}),
            TextSegment(content="The new Macbook Pro has an M4 chip.", segment_id="apple_2", metadata={"category": "tech"}),
            TextSegment(content="Bananas are rich in potassium.", segment_id="banana_1", metadata={"category": "food"})
        ]
        
        print(f"Adding {len(segments)} segments to Chroma...")
        vector_index.add_segments(segments)
        
        # Search without filter
        query = "Tell me about fruit"
        print(f"\nSearching for: '{query}'")
        results = vector_index.similarity_search(query, k=2)
        for r in results:
            print(f"  -> [{r.metadata.get('category')}] {r.content}")
            
        # Search with exact match filter
        print(f"\nSearching for: '{query}' (Filtered to category=tech)")
        results = vector_index.similarity_search(query, k=2, filter_dict={"category": "tech"})
        for r in results:
            print(f"  -> [{r.metadata.get('category')}] {r.content}")
            
    except Exception as e:
        print(f"Example failed (Make sure you ran `pip install chromadb` and have an OpenAI key): {e}")

if __name__ == "__main__":
    example_chroma_vectorstore()

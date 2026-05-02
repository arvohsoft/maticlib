import os
from maticlib.embeddings.openai import OpenAIEmbeddings
from maticlib.vectorstores.milvus import MilvusVectorIndex
from maticlib.core.text.models import TextSegment

from dotenv import load_dotenv
load_dotenv()

def example_milvus_vectorstore():
    print("--- Milvus (Lite) Vector Store Example ---")
    try:
        # Initialize Embeddings
        embeddings = OpenAIEmbeddings()
        
        # Setup Milvus Lite DB file
        db_file = "./milvus_demo.db"
        if os.path.exists(db_file):
            os.remove(db_file)
            
        print(f"Initializing MilvusVectorIndex at {db_file}...")
        vector_index = MilvusVectorIndex(
            embeddings=embeddings,
            collection_name="demo_collection",
            uri=db_file
        )
        
        # Add segments
        segments = [
            TextSegment(content="SpaceX launched a new rocket today.", segment_id="space_1", metadata={"topic": "space", "year": 2026}),
            TextSegment(content="The new Mars rover found water.", segment_id="space_2", metadata={"topic": "space", "year": 2026}),
            TextSegment(content="Local baker wins national pie contest.", segment_id="news_1", metadata={"topic": "local", "year": 2026})
        ]
        
        print(f"Adding {len(segments)} segments to Milvus...")
        vector_index.add_segments(segments)
        
        # Search without filter
        query = "Tell me about space exploration"
        print(f"\nSearching for: '{query}'")
        results = vector_index.similarity_search(query, k=2)
        for r in results:
            print(f"  -> [{r.metadata.get('topic')}] {r.content}")
            
        # Search with exact match filter
        print(f"\nSearching for: '{query}' (Filtered to topic=local)")
        results = vector_index.similarity_search(query, k=2, filter_dict={"topic": "local"})
        for r in results:
            print(f"  -> [{r.metadata.get('topic')}] {r.content}")
            
    except Exception as e:
        print(f"Example failed (Make sure you ran `pip install pymilvus` and have an OpenAI key): {e}")

if __name__ == "__main__":
    example_milvus_vectorstore()

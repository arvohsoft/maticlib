import os
from maticlib.embeddings.openai import OpenAIEmbeddings
from maticlib.vectorstores.milvus import MilvusVectorIndex
from maticlib.core.text.models import TextSegment

from dotenv import load_dotenv

load_dotenv()


def example_milvus_server_vectorstore():
    print("--- Milvus (Server) Vector Store Example ---")
    try:
        # Initialize Embeddings
        embeddings = OpenAIEmbeddings()

        # Connect to a Milvus Server running at http://localhost:19530
        # (This uses the standard gRPC port 19530 required by pymilvus)
        server_uri = "http://localhost:19530"

        print(f"Connecting to MilvusVectorIndex at {server_uri}...")
        vector_index = MilvusVectorIndex(
            embeddings=embeddings,
            collection_name="server_demo_collection",
            uri=server_uri,
        )

        # Add segments
        segments = [
            TextSegment(
                content="Quantum computing uses qubits.",
                segment_id="qc_1",
                metadata={"topic": "science"},
            ),
            TextSegment(
                content="AI agents can automate complex workflows.",
                segment_id="ai_1",
                metadata={"topic": "tech"},
            ),
            TextSegment(
                content="The Mediterranean diet is healthy.",
                segment_id="food_1",
                metadata={"topic": "health"},
            ),
        ]

        print(f"Adding {len(segments)} segments to Milvus Server...")
        vector_index.add_segments(segments)

        # Search
        query = "Tell me about artificial intelligence"
        print(f"\nSearching for: '{query}'")
        results = vector_index.similarity_search(query, k=2)
        for r in results:
            print(f"  -> [{r.metadata.get('topic')}] {r.content}")

    except Exception as e:
        print(
            f"Example failed (Make sure your Milvus server is running at http://localhost:19530): {e}"
        )


if __name__ == "__main__":
    example_milvus_server_vectorstore()

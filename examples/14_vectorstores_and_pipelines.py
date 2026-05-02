import os
from maticlib.embeddings.openai import OpenAIEmbeddings
from maticlib.llm.openai import OpenAIClient
from maticlib.vectorstores.in_memory import InMemoryVectorIndex
from maticlib.core.text.models import TextSegment
from maticlib.pipelines.rag_pipeline import RAGPipeline
from maticlib.observability.trace import PipelineTrace
from maticlib.observability.callbacks import LoggingCallbackHandler

from dotenv import load_dotenv
load_dotenv()

def example_in_memory_rag_pipeline():
    print("--- 1. In-Memory RAG Pipeline ---")
    try:
        # Initialize standard clients
        llm = OpenAIClient()
        embeddings = OpenAIEmbeddings()
        
        # 1. Setup the Vector Store
        vector_index = InMemoryVectorIndex(embeddings=embeddings)
        
        # Add some dummy segments
        segments = [
            TextSegment(content="Maticlib is built in Python and supports OpenAI and Gemini.", segment_id="1"),
            TextSegment(content="The RAG pipeline natively supports Hybrid Retrieval.", segment_id="2"),
            TextSegment(content="MaticGraph is the stateful workflow engine behind Maticlib.", segment_id="3")
        ]
        print("Embedding and adding segments to vector index...")
        vector_index.add_segments(segments)
        
        # 2. Setup the RAG Pipeline
        print("Configuring RAG Pipeline (Hybrid + Query Transform enabled)...")
        pipeline = RAGPipeline(
            llm_client=llm,
            vector_index=vector_index,
            prompt_name="rag_qa",
            use_hybrid=True, # Will use HybridRetriever internally
            use_query_transform=True # Will use QueryTransformer internally
        )
        
        # 3. Execute with Observability Tracing
        trace = PipelineTrace(pipeline_name="Memory_RAG")
        handler = LoggingCallbackHandler()
        handler.on_pipeline_start(trace)
        
        question = "What languages and models does Maticlib support?"
        print(f"\nQuestion: {question}")
        
        # Run generation
        answer = pipeline.generate(
            question=question,
            k=2,
            keywords=["Python", "OpenAI"], # Optional keyword boosts for hybrid
            trace=trace
        )
        
        handler.on_pipeline_end(trace)
        
        print("\nFinal Answer:\n", answer)
        
    except Exception as e:
        print(f"Failed to run example (missing API keys or numpy?): {e}")

if __name__ == "__main__":
    example_in_memory_rag_pipeline()

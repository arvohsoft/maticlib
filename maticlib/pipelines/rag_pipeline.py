from typing import List, Optional, Dict, Any
from maticlib.core.text.models import TextSegment
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.prompts.registry import PromptRegistry
from maticlib.core.retrieval.hybrid import HybridRetriever
from maticlib.core.retrieval.transformers import QueryTransformer
from maticlib.observability.trace import PipelineTrace, StepTrace
import time

class RAGPipeline:
    """
    End-to-end RAG pipeline coordinating retrieval and generation.
    """
    def __init__(
        self,
        llm_client: Any,
        vector_index: BaseVectorIndex,
        prompt_name: str = "rag_qa",
        use_hybrid: bool = False,
        use_query_transform: bool = False
    ):
        self.llm_client = llm_client
        self.vector_index = vector_index
        self.prompt_template = PromptRegistry.get(prompt_name)
        self.use_hybrid = use_hybrid
        self.use_query_transform = use_query_transform
        
        self.retriever = HybridRetriever(self.vector_index) if use_hybrid else None
        self.transformer = QueryTransformer(self.llm_client) if use_query_transform else None

    def generate(
        self, 
        question: str, 
        k: int = 4, 
        keywords: Optional[List[str]] = None,
        trace: Optional[PipelineTrace] = None
    ) -> str:
        """
        Executes the RAG pipeline.
        """
        # Step 1: Query Transformation (Optional)
        search_queries = [question]
        if self.transformer:
            transform_step = StepTrace(step_name="Query_Transform") if trace else None
            try:
                variations = self.transformer.generate_variations(question, n=2)
                search_queries.extend(variations)
            finally:
                if trace and transform_step:
                    transform_step.end_time = time.time()
                    trace.add_step(transform_step)

        # Step 2: Retrieval
        retrieve_step = StepTrace(step_name="Retrieval") if trace else None
        all_segments = []
        try:
            for q in set(search_queries):
                if self.retriever:
                    segs = self.retriever.retrieve(q, k=k, keywords=keywords)
                else:
                    segs = self.vector_index.similarity_search(q, k=k)
                all_segments.extend(segs)
            
            # Simple deduplication
            seen = set()
            unique_segments = []
            for s in all_segments:
                if s.segment_id not in seen:
                    seen.add(s.segment_id)
                    unique_segments.append(s)
            
            # Keep top k
            unique_segments = unique_segments[:k]
        finally:
            if trace and retrieve_step:
                retrieve_step.end_time = time.time()
                trace.add_step(retrieve_step)

        # Step 3: Formatting & Generation
        gen_step = StepTrace(step_name="Generation") if trace else None
        try:
            context = "\n\n".join([f"--- Context ---\n{s.content}" for s in unique_segments])
            prompt = self.prompt_template.format(context=context, question=question)
            
            res = self.llm_client.complete(prompt)
            
            # Extract token stats if available
            if hasattr(res, 'prompt_tokens') and trace and gen_step:
                gen_step.prompt_tokens = getattr(res, 'prompt_tokens', 0)
                gen_step.completion_tokens = getattr(res, 'completion_tokens', 0)
                gen_step.total_tokens = getattr(res, 'total_tokens', 0)
            
            return self.llm_client.get_text_response(res)
        finally:
            if trace and gen_step:
                gen_step.end_time = time.time()
                trace.add_step(gen_step)

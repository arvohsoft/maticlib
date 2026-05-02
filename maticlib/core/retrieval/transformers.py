from typing import List

class QueryTransformer:
    """
    Transforms or expands a query for better retrieval.
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def generate_variations(self, query: str, n: int = 3) -> List[str]:
        """
        Uses an LLM to generate variations of the query.
        """
        if not self.llm_client:
            # Fallback if no LLM provided: just return the query itself
            return [query]
            
        prompt = f"Generate {n} different variations of the following search query to improve retrieval from a vector database. Return one variation per line. Query: {query}"
        
        try:
            res = self.llm_client.complete(prompt)
            text = self.llm_client.get_text_response(res)
            variations = [line.strip("- *").strip() for line in text.split("\n") if line.strip()]
            return variations[:n] if variations else [query]
        except Exception:
            return [query]

import os
from typing import List, Optional
import httpx
from maticlib.embeddings.base import BaseEmbeddings

class MistralEmbeddings(BaseEmbeddings):
    """
    Client for interacting with Mistral AI Embedding models.
    
    Args:
        model: The Mistral embedding model to use. Defaults to "mistral-embed".
        api_key: Your Mistral API key. Falls back to MISTRAL_API_KEY environment variable.
        verbose: If True, prints status messages to console.
    """

    def __init__(
        self,
        model: str = "mistral-embed",
        api_key: Optional[str] = None,
        verbose: bool = True,
    ):
        api_key = api_key or os.getenv("MISTRAL_API_KEY", "")
        api_key = (api_key or "").strip()
        if not api_key:
            raise ValueError(
                "Mistral API key is missing. Please provide it via the 'api_key' "
                "argument or set the MISTRAL_API_KEY environment variable."
            )
        self.api_key = api_key
        self.model = model
        self.verbose = verbose
        self.base_url = "https://api.mistral.ai/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document strings."""
        payload = {
            "model": self.model,
            "input": texts,
        }

        try:
            response = httpx.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            if self.verbose:
                print(f"Mistral Embeddings Status: {response.status_code}")

            data = response.json()
            # Mistral returns a list of objects with 'embedding' and 'index'
            embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
            return embeddings

        except Exception as e:
            if self.verbose:
                print(f"Error in Mistral embed_documents: {e}")
            raise

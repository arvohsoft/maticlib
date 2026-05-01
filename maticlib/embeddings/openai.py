import os
from typing import List, Optional, Union
import httpx
from maticlib.embeddings.base import BaseEmbeddings
from maticlib.embeddings.models import EmbedQueryResponse, EmbedDocumentsResponse

class OpenAIEmbeddings(BaseEmbeddings):
    """
    Client for interacting with OpenAI Embedding models.
    
    Args:
        model: The OpenAI embedding model to use. Defaults to "text-embedding-3-small".
        api_key: Your OpenAI API key. Falls back to OPENAI_API_KEY environment variable.
        dimensions: The number of dimensions the resulting output embeddings should have.
            Only supported in text-embedding-3 and later models.
        verbose: If True, prints status messages to console.
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        dimensions: Optional[int] = None,
        verbose: bool = True,
    ):
        super().__init__()
        api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        api_key = (api_key or "").strip()
        if not api_key:
            raise ValueError(
                "OpenAI API key is missing. Please provide it via the 'api_key' "
                "argument or set the OPENAI_API_KEY environment variable."
            )
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions
        self.verbose = verbose
        self.base_url = "https://api.openai.com/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def embed_query(self, text: str) -> EmbedQueryResponse:
        """Embed a single query string."""
        docs_res = self.embed_documents([text])
        return EmbedQueryResponse(
            vector=docs_res.vectors[0],
            prompt_tokens=docs_res.prompt_tokens,
            total_tokens=docs_res.total_tokens,
            model=docs_res.model,
            raw_response=docs_res.raw_response,
        )

    def embed_documents(self, texts: List[str]) -> EmbedDocumentsResponse:
        """Embed a list of document strings."""
        payload = {
            "model": self.model,
            "input": texts,
        }
        if self.dimensions:
            payload["dimensions"] = self.dimensions

        try:
            response = httpx.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            if self.verbose:
                print(f"OpenAI Embeddings Status: {response.status_code}")

            data = response.json()
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            total_tokens = usage.get("total_tokens", prompt_tokens)

            # OpenAI returns data sorted by index in the 'data' list
            embeddings = [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]
            
            return EmbedDocumentsResponse(
                vectors=embeddings,
                prompt_tokens=prompt_tokens,
                total_tokens=total_tokens,
                model=data.get("model", self.model),
                raw_response=data
            )

        except httpx.HTTPStatusError as e:
            if self.verbose:
                print(f"HTTP Error: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            raise
        except Exception:
            raise

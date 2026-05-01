import os
from typing import Any, Dict, List, Optional, Union
import httpx
from maticlib.embeddings.base import BaseEmbeddings

class GoogleGenAIEmbeddings(BaseEmbeddings):
    """
    Client for interacting with Google's Generative AI (Gemini) Embedding models.
    
    Args:
        model: The Gemini embedding model to use. Defaults to "gemini-embedding-001".
        api_key: Your Google AI API key. Falls back to GOOGLE_API_KEY or GEMINI_API_KEY.
        task_type: The type of task the embedding will be used for. 
            Common values: "RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT", "SEMANTIC_SIMILARITY".
        verbose: If True, prints status messages to console.
    """

    def __init__(
        self,
        model: str = "gemini-embedding-001",
        api_key: Optional[str] = None,
        task_type: str = "RETRIEVAL_DOCUMENT",
        verbose: bool = True,
    ):
        api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
        api_key = (api_key or "").strip()
        if not api_key:
            raise ValueError(
                "Google Gemini API key is missing. Please provide it via the 'api_key' "
                "argument or set the GOOGLE_API_KEY environment variable."
            )
        self.api_key = api_key
        # Ensure model has 'models/' prefix if not present
        if not model.startswith("models/"):
            model = f"models/{model}"
        self.model = model
        self.task_type = task_type
        self.verbose = verbose
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        url = f"{self.base_url}/{self.model}:embedContent"
        payload = {
            "model": self.model,
            "content": {"parts": [{"text": text}]},
            "taskType": "RETRIEVAL_QUERY" # Override for queries
        }

        try:
            response = httpx.post(url, headers=self.headers, json=payload, timeout=60.0)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Google Embeddings Status: {response.status_code}")

            data = response.json()
            return data["embedding"]["values"]

        except Exception as e:
            if self.verbose:
                print(f"Error in Google embed_query: {e}")
            raise

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document strings using batchEmbedContents."""
        url = f"{self.base_url}/{self.model}:batchEmbedContents"
        
        requests = []
        for text in texts:
            requests.append({
                "model": self.model,
                "content": {"parts": [{"text": text}]},
                "taskType": self.task_type
            })
            
        payload = {"requests": requests}

        try:
            response = httpx.post(url, headers=self.headers, json=payload, timeout=60.0)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Google Batch Embeddings Status: {response.status_code}")

            data = response.json()
            return [item["values"] for item in data["embeddings"]]

        except Exception as e:
            if self.verbose:
                print(f"Error in Google embed_documents: {e}")
            raise

from typing import Any, Dict, List
import httpx
import os


class MistralClient:
    def __init__(
        self,
        model: str = "mistral-medium-latest",
        api_key: str = os.getenv("MISTRAL_API_KEY", ""),
        verbose: bool = True
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.mistral.ai/v1"
        self.verbose = verbose
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def complete(self, prompt: str | List[Dict[str, str]]) -> httpx.Response:
        """
        Chat completion with Mistral AI
        
        Args:
            prompt: Either a string prompt or a list of message dictionaries
                   String example: "What is the best French cheese?"
                   List example: [{"role": "user", "content": "Hello"}]
            
        Returns:
            httpx.Response object containing the API response
        """
        url = f"{self.base_url}/chat/completions"
        
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        try:
            response = httpx.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Status: {response.status_code}")
                
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
    
    async def async_complete(self, prompt: str | List[Dict[str, str]]) -> httpx.Response:
        """
        Async chat completion with Mistral AI
        
        Args:
            prompt: Either a string prompt or a list of message dictionaries
                   String example: "What is the best French cheese?"
                   List example: [{"role": "user", "content": "Hello"}]
            
        Returns:
            httpx.Response object containing the API response
        """
        url = f"{self.base_url}/chat/completions"
        
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                
                if self.verbose:
                    print(f"Status: {response.status_code}")
                    
                return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
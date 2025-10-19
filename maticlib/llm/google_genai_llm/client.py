from typing import Any, Dict
import httpx
import os

class GoogleGenAIClient:
    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key: str = os.getenv("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        thinking_budget: int = 0,
        verbose: bool = True
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.verbose = verbose
        self.headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        self.thinking_budget = thinking_budget
    
    def complete(self, prompt: str) -> Dict[str, Any]:
        """
        Basic content generation - converts first curl example
        
        Args:
            prompt: The text prompt to send to the model
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        if isinstance(prompt, str):
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
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
            
    async def async_complete(self, prompt: str) -> Dict[str, Any]:
        """
        Basic content generation - converts first curl example
        
        Args:
            prompt: The text prompt to send to the model
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        if isinstance(prompt, str):
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
            
            try:
                client = httpx.AsyncClient()
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                
                if self.verbose:
                    print(f"Status: {response.status_code}")
                    
                return response
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise
from __future__ import annotations
import httpx

class BaseLLMClient:
    """
    Base class for LLM clients.
    
    Provides a template for synchronous and asynchronous content generation
    across different LLM providers.
    
    Args:
        inference_url (str): The endpoint URL for the LLM API.
        header (dict, optional): HTTP headers for the request (e.g., Auth).
        model (str): The name/ID of the model to use.
        payload (dict, optional): Default payload structure for the API.
        verbose (bool): If True, prints status and response information.
    """
    def __init__(
        self,
        inference_url="",
        header="",
        model="",
        payload="",
        verbose=True
    ):
        self.url = inference_url
        self.headers = header if header else {}
        self.model = model
        self.payload = payload if payload else {}
        self.verbose = verbose

    def complete(self, input: str|list):
        """
        Send a synchronous completion request to the LLM.
        
        Args:
            input (str | list): The prompt string or list of messages to send.
            
        Returns:
            httpx.Response: The raw HTTP response from the API.
            
        Raises:
            Exception: If the request fails or payload formatting errors occur.
        """
        try:
            payload = getattr(self, 'payload', {}).copy() if isinstance(getattr(self, 'payload', {}), dict) else {}
            payload["model"] = self.model
            if isinstance(input, str):
                if "messages" not in payload or not payload["messages"]:
                    payload["messages"] = [{"role": "user", "content": ""}]
                payload["messages"][-1]["content"] = input
            
            response = httpx.post(self.url, headers=self.headers, json=payload)
            if self.verbose:
                print(response)
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            
    async def async_complete(self, input: str|list):
        """
        Send an asynchronous completion request to the LLM.
        
        Args:
            input (str | list): The prompt string or list of messages to send.
            
        Returns:
            httpx.Response: The raw HTTP response from the API.
            
        Raises:
            Exception: If the request fails or payload formatting errors occur.
        """
        try:
            payload = getattr(self, 'payload', {}).copy() if isinstance(getattr(self, 'payload', {}), dict) else {}
            payload["model"] = self.model
            if isinstance(input, str):
                if "messages" not in payload or not payload["messages"]:
                    payload["messages"] = [{"role": "user", "content": ""}]
                payload["messages"][-1]["content"] = input
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.url, headers=self.headers, json=payload)
                if self.verbose:
                    print(response)
                return response
        except Exception as e:
            import traceback
            traceback.print_exc()
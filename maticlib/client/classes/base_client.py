from __future__ import annotations
import httpx

class BaseLLMClient:
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
        try:
            payload["model"] = self.model
            if type(input) == type("string"):
            
                payload = self.payload
                payload["messages"][-1]["content"] = input
            response = httpx.post(self.url, headers=self.headers, json=payload)
            if self.verbose:
                print(response)
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            
    def async_complete(self, input: str|list):
        try:
            payload["model"] = self.model
            if type(input) == type("string"):
            
                payload = self.payload
                payload["messages"][-1]["content"] = input
                client = httpx.AsyncClient()
            response = client.post(self.url, headers=self.headers, json=payload)
            if self.verbose:
                print(response)
            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
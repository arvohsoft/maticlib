from typing import Any, Dict, List, Union

from maticlib.llm.google_genai.gemini_classes import GeminiResponse
from ..classes.base_client import BaseLLMClient
from ...core.messages import SystemMessage, HumanMessage, AIMessage
import httpx
import os

class GoogleGenAIClient(BaseLLMClient):
    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key: str = os.getenv("GOOGLE_API_KEY", "GEMINI_API_KEY"),
        thinking_budget: int = 0,
        verbose: bool = True,
        return_raw: bool = False
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
        self.return_raw = return_raw  # Option to return raw JSON response or Pydantic model
        
    def _format_messages(self, input: Union[str, List[Union[Dict, HumanMessage, SystemMessage, AIMessage]]]):
        if isinstance(input, str):
            # Return a list of messages, NOT wrapped in "contents"
            return [
                {
                    "parts": [{"text": input}]
                }
            ]
        
        elif isinstance(input, list):
            formatted_messages = []
            
            for message in input:
                # Handle dictionary format
                if isinstance(message, dict):
                    role = message.get("role")
                    content = message.get("content")
                    
                    if role is None:
                        raise ValueError(f"Message dictionary must have 'role' key: {message}")
                    
                    if not isinstance(content, str):
                        raise TypeError(f"Message content must be a string, got {type(content)}")
                    
                    # Map roles to Gemini format
                    if role in ["user", "system"]:
                        gemini_role = "user"
                    elif role in ["assistant", "model"]:
                        gemini_role = "model"
                    else:
                        gemini_role = "user"  # Default to user
                    
                    formatted_messages.append({
                        "role": gemini_role,
                        "parts": [{"text": content}]
                    })
                
                # Handle message objects
                elif isinstance(message, (HumanMessage, SystemMessage)):
                    formatted_messages.append({
                        "role": "user",
                        "parts": [{"text": message.content}]
                    })
                
                elif isinstance(message, AIMessage):
                    formatted_messages.append({
                        "role": "model",
                        "parts": [{"text": message.content}]
                    })
                
                else:
                    raise TypeError(f"Unsupported message type: {type(message)}")
            
            return formatted_messages
        
        else:
            raise TypeError(f"Input must be str or list, got {type(input)}")
    
    def _parse_response(self, response: httpx.Response) -> Union[GeminiResponse, Dict[str, Any]]:
        """
        Parse the HTTP response into a Pydantic model or raw dict
        
        Args:
            response: The httpx Response object
            
        Returns:
            Either a GeminiResponse Pydantic model or raw response dict
        """
        response_data = response.json()
        
        # Add metadata that might not be in the response
        response_data['responseId'] = response.headers.get('X-Response-Id', 'unknown')
        response_data['modelVersion'] = self.model
        
        if self.return_raw:
            return response_data
        

        try:
            return GeminiResponse(**response_data)
        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to parse response into Pydantic model: {e}")
                print("Returning raw response instead")
            return response_data
    
    def complete(self, input: Union[str, List]) -> Union[GeminiResponse, Dict[str, Any]]:
        """
        Basic content generation with Pydantic response model
        
        Args:
            input: The text input or list of messages to send to the model
            
        Returns:
            GeminiResponse Pydantic model (or dict if return_raw=True)
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        try:
            # Format messages
            formatted_messages = self._format_messages(input)
            
            payload = {
                "contents": formatted_messages
            }
            
            # Add thinking budget if configured
            if self.thinking_budget > 0:
                payload["generationConfig"] = {
                    "thinkingBudget": self.thinking_budget
                }
            
            # Make request
            response = httpx.post(url, headers=self.headers, json=payload, timeout=30.0)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Status: {response.status_code}")
            
            # Parse and return response
            return self._parse_response(response)
            
        except httpx.HTTPStatusError as e:
            if self.verbose:
                print(f"HTTP Error: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            raise
        except Exception as e:
            if self.verbose:
                import traceback
                traceback.print_exc()
            raise
    
    def complete(self, input: str) -> Dict[str, Any]:
        """
        Basic content generation - converts first curl example
        
        Args:
            input: The text input to send to the model
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        formatted_messages = self._format_messages(input=input)
        payload = {
            "contents": formatted_messages
        }
        
        if self.thinking_budget > 0:
            payload["generationConfig"] = {
                "thinkingBudget": self.thinking_budget
            }
        
        try:
            response = httpx.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Status: {response.status_code}")
                
            return self._parse_response(response=response)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
            
    async def async_complete(self, input: str) -> Dict[str, Any]:
        """
        Basic content generation - converts first curl example
        
        Args:
            input: The text input to send to the model
            
        Returns:
            Dictionary containing the API response
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        formatted_messages = self._format_messages(input=input)
        payload = {
            "contents": formatted_messages
        }
        
        if self.thinking_budget > 0:
            payload["generationConfig"] = {
                "thinkingBudget": self.thinking_budget
            }
                   
        try:
            client = httpx.AsyncClient()
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Status: {response.status_code}")
                
            return self._parse_response(response=response)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
    
    def get_text_response(self, response: Union[GeminiResponse, Dict[str, Any]]) -> str:
        """
        Helper method to extract text from response
        
        Args:
            response: GeminiResponse model or raw dict
            
        Returns:
            Extracted text content
        """
        if isinstance(response, GeminiResponse):
            return response.content or ""
        
        # Handle raw dict response
        try:
            candidates = response.get('candidates', [])
            if candidates:
                parts = candidates[0].get('content', {}).get('parts', [])
                texts = [part.get('text', '') for part in parts if 'text' in part]
                return ' '.join(texts)
        except Exception:
            raise
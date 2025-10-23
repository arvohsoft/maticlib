from typing import Any, Dict, List, Union
import httpx
import os
from maticlib.client.classes.base_client import BaseLLMClient
from maticlib.llm.mistral.mistral_classes import MistralResponse
from maticlib.messages import SystemMessage, HumanMessage, AIMessage


class MistralClient(BaseLLMClient):
    def __init__(
        self,
        model: str = "mistral-medium-latest",
        system_instruct: str|SystemMessage|None = None,
        api_key: str = os.getenv("MISTRAL_API_KEY", ""),
        verbose: bool = True,
        return_raw: bool = False
    ):
        self.api_key = api_key
        self.model = model
        self.system_instruct = system_instruct
        self.base_url = "https://api.mistral.ai/v1"
        self.verbose = verbose
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.return_raw = return_raw  # Option to return raw JSON response or Pydantic model
        
    def _format_messages(self, input: Union[str, List[Union[Dict, HumanMessage, SystemMessage, AIMessage]]]):
        """
        Format messages to Mistral API format
        
        Mistral expects: [{"role": "user|assistant|system", "content": "text"}]
        """
        if isinstance(input, str):
            # Return a list of messages for Mistral
            return [
                {
                    "role": "user",
                    "content": input
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
                    
                    # Map roles to Mistral format (system, user, assistant)
                    if role in ["user", "human"]:
                        mistral_role = "user"
                    elif role in ["assistant", "ai", "model"]:
                        mistral_role = "assistant"
                    elif role == "system":
                        mistral_role = "system"
                    else:
                        mistral_role = "user"  # Default to user
                    
                    formatted_messages.append({
                        "role": mistral_role,
                        "content": content
                    })
                
                # Handle message objects
                elif isinstance(message, (HumanMessage, SystemMessage)):
                    role = "system" if isinstance(message, SystemMessage) else "user"
                    formatted_messages.append({
                        "role": role,
                        "content": message.content
                    })
                
                elif isinstance(message, AIMessage):
                    formatted_messages.append(
                            {
                            "role": "assistant",
                            "content": message.content
                        }
                    )
                
                else:
                    raise TypeError(f"Unsupported message type: {type(message)}")
            
            return formatted_messages
        
        else:
            raise TypeError(f"Input must be str or list, got {type(input)}")
    
    def __format__system_instruction(self):
        system_instruct = self.system_instruct
        if isinstance(system_instruct, str):
            return system_instruct
        elif isinstance(system_instruct, SystemMessage):
            return system_instruct.content
    
    def _parse_response(self, response: httpx.Response) -> Union[MistralResponse, Dict[str, Any]]:
        """
        Parse the HTTP response into a Pydantic model or raw dict
        
        Args:
            response: The httpx Response object
            
        Returns:
            Either a MistralResponse Pydantic model or raw response dict
        """
        response_data = response.json()
        
        # Add model version metadata
        response_data['modelVersion'] = self.model
        
        if self.return_raw:
            return response_data
        
        try:
            return MistralResponse(**response_data)
        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to parse response into Pydantic model: {e}")
                print("Returning raw response instead")
            return response_data
    
    def complete(self, input: Union[str, List]) -> Union[MistralResponse, Dict[str, Any]]:
        """
        Basic content generation with Pydantic response model
        
        Args:
            input: The text input or list of messages to send to the model
            
        Returns:
            MistralResponse Pydantic model (or dict if return_raw=True)
        """
        url = f"{self.base_url}/chat/completions"
        
        try:
            # Format messages
            formatted_messages = self._format_messages(input)
            
            payload = {
                "model": self.model,
                "messages": formatted_messages
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
            
    async def async_complete(self, input: Union[str, List]) -> Union[MistralResponse, Dict[str, Any]]:
        """
        Async content generation with Pydantic response model
        
        Args:
            input: The text input or list of messages to send to the model
            
        Returns:
            MistralResponse Pydantic model (or dict if return_raw=True)
        """
        url = f"{self.base_url}/chat/completions"
        
        try:
            # Format messages
            formatted_messages = self._format_messages(input)
            
            payload = {
                "model": self.model,
                "messages": formatted_messages
            }
            
            # Make async request
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload, timeout=30.0)
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
    
    def get_text_response(self, response: Union[MistralResponse, Dict[str, Any]]) -> str:
        """
        Helper method to extract text from response
        
        Args:
            response: MistralResponse model or raw dict
            
        Returns:
            Extracted text content
        """
        if isinstance(response, MistralResponse):
            return response.content or ""
        
        # Handle raw dict response
        try:
            choices = response.get('choices', [])
            if choices:
                message = choices[0].get('message', {})
                content = message.get('content', '')
                return content
        except Exception:
            raise
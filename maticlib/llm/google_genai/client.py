from typing import Any, Dict, List, Optional, Type, Union, Callable
from pydantic import BaseModel

from maticlib.client.classes.base_client import BaseLLMClient
from maticlib.llm.google_genai.gemini_classes import GeminiResponse
from maticlib.messages import SystemMessage, HumanMessage, AIMessage
import httpx
import os

class GoogleGenAIClient(BaseLLMClient):
    """
    Client for interacting with Google's Generative AI (Gemini) models.
    
    Inherits from BaseLLMClient and implements Gemini-specific message 
    formatting and response parsing.
    
    Args:
        model (str): The name of the Gemini model to use. 
            Defaults to "gemini-2.5-flash".
        system_instruct (str | SystemMessage, optional): Default instructions 
            to prepend to all conversations.
        api_key (str): Your Google AI API key.
        thinking_budget (int): Optional token budget for model reasoning/thinking.
        verbose (bool): If True, prints status messages to console.
        return_raw (bool): If True, returns the raw dict response instead of a GeminiResponse model.
    """
    def __init__(
        self,
        model: str = "gemini-2.5-flash-lite",
        system_instruct: str|SystemMessage|None = None,
        api_key: Optional[str] = None,
        thinking_budget: int = 0,
        verbose: bool = True,
        return_raw: bool = False
    ):
        api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
        api_key = (api_key or "").strip()
        if not api_key:
            raise ValueError(
                "Google Gemini API key is missing. Please provide it via the 'api_key' "
                "argument or set the GOOGLE_API_KEY environment variable."
            )
        self.api_key = api_key
        self.model = model
        self.system_instruct = system_instruct
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.verbose = verbose
        self.headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        self.thinking_budget = thinking_budget
        self.return_raw = return_raw  # Option to return raw JSON response or Pydantic model
        
    def _format_messages(self, input: Union[str, List[Union[Dict, HumanMessage, SystemMessage, AIMessage]]]):
        """
        Formats various input types into the standard Gemini API content format.
        
        Args:
            input (str | list): A simple string, a list of message objects, 
                or a list of dictionaries with 'role' and 'content'.
                
        Returns:
            list: A list of dictionaries ready for the Gemini 'contents' payload.
            
        Raises:
            ValueError: If a dictionary message is missing a 'role'.
            TypeError: If input types are unsupported.
        """
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
    
    def _format__system_instruction(self):
        system_instruct = self.system_instruct
        if isinstance(system_instruct, str):
            return system_instruct
        elif isinstance(system_instruct, SystemMessage):
            return system_instruct.content
        return None
    
    def _parse_response(self, response: httpx.Response) -> Union[GeminiResponse, Dict[str, Any]]:
        """
        Parses the JSON response from Gemini into a structured model.
        
        Args:
            response (httpx.Response): The raw HTTP response.
            
        Returns:
            GeminiResponse | dict: The parsed response model, or a raw dictionary 
            if `return_raw` is set to True.
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
    
    def complete(
        self, 
        input: Union[str, List],
        response_model: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Callable]] = None
    ) -> Union[GeminiResponse, Dict[str, Any]]:
        """
        Sends a synchronous generation request to Gemini.
        
        Args:
            input (str | list): The user prompt or conversation history.
            response_model (Type[BaseModel], optional): A Pydantic model to 
                parse the output into.
            tools (list, optional): A list of tool functions decorated with @tool.
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        try:
            # Inject structure instructions if requested
            input = self._inject_runtime_instructions(input, response_model)
            
            # Format messages
            formatted_messages = self._format_messages(input)
            
            payload = {}
            
            # Handle tools
            if tools:
                payload["tools"] = self._format_tools(tools)
            
            if self.system_instruct:
                self.system_instruct = self._format__system_instruction()

                payload["system_instruction"] = {
                    "parts": [
                        {
                        "text": self.system_instruct
                        }
                    ]
                }
                
            payload["contents"] = formatted_messages
            
            # Add thinking budget if configured
            if self.thinking_budget > 0:
                payload["generationConfig"] = {
                    "thinkingBudget": self.thinking_budget
                }
            
            # Make request
            response = httpx.post(url, headers=self.headers, json=payload, timeout=60.0)
            response.raise_for_status()
            
            if self.verbose:
                print(f"Status: {response.status_code}")  
                              
            result = self._parse_response(response)
            self._apply_response_model(result, response_model)
            return result
            
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
            
    async def async_complete(
        self, 
        input: str,
        response_model: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Callable]] = None
    ) -> Union[GeminiResponse, Dict[str, Any]]:
        """
        Sends an asynchronous generation request to Gemini.
        
        Args:
            input (str): The text input to send to the model.
            response_model (Type[BaseModel], optional): A Pydantic model to 
                parse the output into.
            tools (list, optional): A list of tool functions decorated with @tool.
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        # Inject structure instructions if requested
        input = self._inject_runtime_instructions(input, response_model)
        
        formatted_messages = self._format_messages(input=input)
        
        payload = {}
        
        # Handle tools
        if tools:
            payload["tools"] = self._format_tools(tools)
            
        if self.system_instruct:
            self.system_instruct = self._format__system_instruction()

            payload["system_instruction"] = {
                "parts": [
                    {
                    "text": self.system_instruct
                    }
                ]
            }
        
        payload["contents"] = formatted_messages
        
        if self.thinking_budget > 0:
            payload["generationConfig"] = {
                "thinkingBudget": self.thinking_budget
            }
                   
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=payload, timeout=60.0)
                response.raise_for_status()
            if self.verbose:
                print(f"Status: {response.status_code}")
                
            result = self._parse_response(response=response)
            self._apply_response_model(result, response_model)
            return result
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
        finally:
            await client.aclose()
    
    def _format_tools(self, tools: List[Callable]) -> List[Dict[str, Any]]:
        """Formats the list of tool functions for Gemini."""
        declarations = []
        for tool_func in tools:
            if hasattr(tool_func, "matic_tool_metadata"):
                metadata = tool_func.matic_tool_metadata
                declarations.append({
                    "name": metadata["name"],
                    "description": metadata["description"],
                    "parameters": metadata["parameters"]
                })
        return [{"function_declarations": declarations}]

    def get_text_response(self, response: Union[GeminiResponse, Dict[str, Any]]) -> str:
        """
        Extracts the primary text content from a Gemini response.
        
        Args:
            response (GeminiResponse | dict): The response to extract from.
            
        Returns:
            str: The extracted text string.
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
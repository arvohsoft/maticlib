"""
OpenAI LLM Client
==================
Provides ``OpenAIClient`` — a high-level wrapper around the OpenAI
Responses API (/v1/responses).

Unlike the older Chat Completions endpoint, the Responses API:
  - Accepts a single ``input`` key (string or list of message dicts)
  - Returns a structured ``output`` list with typed items
  - Exposes richer token-usage metadata (cached tokens, reasoning tokens)

The client follows the exact same interface as ``MistralClient`` and
``GoogleGenAIClient`` (both complete and async_complete, plus
get_text_response) so it can be used as a drop-in replacement.

Supported models (not exhaustive):
  gpt-4o-mini, gpt-4o, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano,
  gpt-4.5, gpt-5, o1, o3, o3-mini, o4-mini, o4, gpt-5.4, ...
"""

import os
from typing import Any, Dict, List, Optional, Type, Union, Callable
from pydantic import BaseModel

import httpx

from maticlib.client.classes.base_client import BaseLLMClient
from maticlib.llm.openai.openai_classes import OpenAIResponse
from maticlib.messages import AIMessage, HumanMessage, SystemMessage


class OpenAIClient(BaseLLMClient):
    """
    Client for interacting with OpenAI models via the Responses API.

    Inherits from ``BaseLLMClient`` and implements OpenAI-specific message
    formatting and response parsing. Supports all current GPT and o-series
    models.

    Args:
        model (str): The OpenAI model to use. Defaults to ``"gpt-4o-mini"``.
            Examples: ``"gpt-4o"``, ``"gpt-4.1"``, ``"o4-mini"``, ``"gpt-5.4"``.
        system_instruct (str | SystemMessage, optional): An optional system /
            developer prompt prepended to every request.
        api_key (str): Your OpenAI API key. Falls back to the
            ``OPENAI_API_KEY`` environment variable.
        verbose (bool): If ``True``, prints HTTP status codes to stdout.
        return_raw (bool): If ``True``, the ``complete`` / ``async_complete``
            methods return the raw ``dict`` instead of an ``OpenAIResponse``
            model.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        system_instruct: Union[str, SystemMessage, None] = None,
        api_key: Optional[str] = None,
        verbose: bool = True,
        return_raw: bool = False,
    ) -> None:
        api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        api_key = (api_key or "").strip()
        if not api_key:
            raise ValueError(
                "OpenAI API key is missing. Please provide it via the 'api_key' "
                "argument or set the OPENAI_API_KEY environment variable."
            )
        self.api_key = api_key
        self.model = model
        self.system_instruct = system_instruct
        self.base_url = "https://api.openai.com/v1"
        self.verbose = verbose
        self.return_raw = return_raw
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _format_input(
        self,
        input: Union[str, List[Union[Dict, HumanMessage, SystemMessage, AIMessage]]],
    ) -> Union[str, List[Dict]]:
        """
        Converts the caller's input into the format expected by /v1/responses.

        The Responses API accepts either:
          - A plain string as the ``input`` value, **or**
          - A list of message dicts: ``[{"role": "user", "content": "..."}]``

        Args:
            input (str | list): A plain string prompt or a list of message
                objects / dicts.

        Returns:
            str | list: The formatted input ready to assign to the payload.

        Raises:
            ValueError: If a dict message is missing a ``role`` key.
            TypeError: If an unsupported message type is encountered.
        """
        # --- plain string — pass through directly ---
        if isinstance(input, str):
            return input

        if not isinstance(input, list):
            raise TypeError(f"input must be str or list, got {type(input)}")

        formatted: List[Dict] = []
        for message in input:
            if isinstance(message, dict):
                role = message.get("role")
                content = message.get("content")
                if role is None:
                    raise ValueError(
                        f"Message dict must have a 'role' key: {message}"
                    )
                if not isinstance(content, str):
                    raise TypeError(
                        f"Message content must be str, got {type(content)}"
                    )
                # Map maticlib role aliases → OpenAI roles
                role_map = {
                    "human": "user",
                    "ai": "assistant",
                    "model": "assistant",
                }
                formatted.append(
                    {"role": role_map.get(role, role), "content": content}
                )
            elif isinstance(message, HumanMessage):
                formatted.append({"role": "user", "content": message.content})
            elif isinstance(message, SystemMessage):
                formatted.append({"role": "developer", "content": message.content})
            elif isinstance(message, AIMessage):
                formatted.append({"role": "assistant", "content": message.content})
            else:
                raise TypeError(f"Unsupported message type: {type(message)}")

        return formatted

    def _build_payload(
        self,
        input: Union[str, List[Union[Dict, HumanMessage, SystemMessage, AIMessage]]],
        tools: Optional[List[Callable]] = None,
    ) -> Dict[str, Any]:
        """
        Builds the full JSON payload for the /v1/responses endpoint.

        Args:
            input (str | list): Raw caller input (string or message list).
            tools (list, optional): A list of tool functions.

        Returns:
            dict: A payload dict ready to be sent as JSON.
        """
        formatted_input = self._format_input(input)

        payload: Dict[str, Any] = {
            "model": self.model,
            "input": formatted_input,
        }

        # Handle tools
        if tools:
            payload["tools"] = self._format_tools(tools)

        # Prepend system/developer instruction when provided
        if self.system_instruct:
            system_text = (
                self.system_instruct
                if isinstance(self.system_instruct, str)
                else self.system_instruct.content
            )
            # The Responses API supports an explicit 'instructions' key which
            # acts as a developer/system prompt regardless of input format.
            payload["instructions"] = system_text

        return payload

    def _parse_response(
        self, response: httpx.Response
    ) -> Union[OpenAIResponse, Dict[str, Any]]:
        """
        Parses the JSON HTTP response into a structured ``OpenAIResponse``.

        Args:
            response (httpx.Response): The raw HTTP response from the API.

        Returns:
            OpenAIResponse | dict: The parsed model, or a raw dict if
            ``return_raw`` is ``True``.
        """
        response_data = response.json()

        if self.return_raw:
            return response_data

        try:
            return OpenAIResponse(**response_data)
        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to parse into OpenAIResponse: {e}")
                print("Returning raw dict instead.")
            return response_data

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def complete(
        self,
        input: Union[str, List],
        response_model: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Callable]] = None,
    ) -> Union[OpenAIResponse, Dict[str, Any]]:
        """
        Sends a synchronous generation request to the OpenAI Responses API.

        Args:
            input (str | list): The user prompt as a plain string, or a
                conversation history as a list of message objects / dicts.
            response_model (Type[BaseModel], optional): A Pydantic model to 
                parse the output into.
            tools (list, optional): A list of tool functions decorated with @tool.
        """
        url = f"{self.base_url}/responses"

        try:
            input = self._inject_runtime_instructions(input, response_model)
            payload = self._build_payload(input, tools=tools)
            response = httpx.post(
                url, headers=self.headers, json=payload, timeout=60.0
            )
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
        except Exception:
            if self.verbose:
                import traceback
                traceback.print_exc()
            raise

    async def async_complete(
        self,
        input: Union[str, List],
        response_model: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Callable]] = None,
    ) -> Union[OpenAIResponse, Dict[str, Any]]:
        """
        Sends an asynchronous generation request to the OpenAI Responses API.

        Args:
            input (str | list): The user prompt as a plain string, or a
                conversation history as a list of message objects / dicts.
            response_model (Type[BaseModel], optional): A Pydantic model to 
                parse the output into.
            tools (list, optional): A list of tool functions decorated with @tool.
        """
        url = f"{self.base_url}/responses"

        try:
            input = self._inject_runtime_instructions(input, response_model)
            payload = self._build_payload(input, tools=tools)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, headers=self.headers, json=payload, timeout=60.0
                )
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
        except Exception:
            if self.verbose:
                import traceback
                traceback.print_exc()
            raise

    def _format_tools(self, tools: List[Callable]) -> List[Dict[str, Any]]:
        """Formats the list of tool functions for OpenAI."""
        formatted = []
        for tool_func in tools:
            if hasattr(tool_func, "matic_tool_metadata"):
                metadata = tool_func.matic_tool_metadata
                formatted.append({
                    "type": "function",
                    "function": {
                        "name": metadata["name"],
                        "description": metadata["description"],
                        "parameters": metadata["parameters"]
                    }
                })
        return formatted

    def get_text_response(
        self, response: Union[OpenAIResponse, Dict[str, Any]]
    ) -> str:
        """
        Extracts the primary text content from an OpenAI response.

        This is a convenience helper so callers do not need to traverse
        the ``output`` list manually.

        Args:
            response (OpenAIResponse | dict): The response returned by
                ``complete`` or ``async_complete``.

        Returns:
            str: The extracted text string, or an empty string if no text
            was found.
        """
        if isinstance(response, OpenAIResponse):
            return response.content or ""

        # Raw dict fallback: walk output items manually
        try:
            for item in response.get("output", []):
                for part in item.get("content", []):
                    if part.get("type") == "output_text" and part.get("text"):
                        return part["text"]
        except Exception:
            raise

        return ""

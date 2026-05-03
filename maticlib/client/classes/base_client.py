from __future__ import annotations
import httpx
from typing import Any, Dict, List, Optional, Type, Union, Callable
from pydantic import BaseModel
from maticlib.core.parsers.pydantic import PydanticResponseParser


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

    def __init__(self, inference_url="", header="", model="", payload="", verbose=True):
        self.url = inference_url
        self.headers = header if header else {}
        self.model = model
        self.payload = payload if payload else {}
        self.verbose = verbose

    # ------------------------------------------------------------------
    # Internal Structured Parsing Helpers
    # ------------------------------------------------------------------

    def _inject_runtime_instructions(
        self, input: Union[str, List], response_model: Optional[Type[BaseModel]]
    ) -> Union[str, List]:
        """Modifies input to include structure instructions if a model is provided."""
        if not response_model:
            return input

        parser = PydanticResponseParser(model=response_model)
        instructions = parser.get_structure_instructions()

        if isinstance(input, str):
            return f"{input}\n\n{instructions}"

        if isinstance(input, list) and len(input) > 0:
            modified_input = [
                msg.copy() if isinstance(msg, dict) else msg for msg in input
            ]
            last_msg = modified_input[-1]
            if isinstance(last_msg, dict) and "content" in last_msg:
                last_msg["content"] = f"{last_msg['content']}\n\n{instructions}"
            elif hasattr(last_msg, "content"):
                last_msg.content = f"{last_msg.content}\n\n{instructions}"
            return modified_input

        return input

    def _apply_response_model(
        self,
        response: LLMResponseBase | Dict[str, Any],
        response_model: Optional[Type[BaseModel]],
    ) -> None:
        """Parses the text response and populates parsed_output if requested."""
        if not response_model or self.return_raw or isinstance(response, dict):
            return

        try:
            text = self.get_text_response(response)
            if text:
                parser = PydanticResponseParser(model=response_model)
                response.parsed_output = parser.parse(text)
        except Exception as e:
            if self.verbose:
                print(f"Warning: Response parsing failed: {e}")

    # ------------------------------------------------------------------
    # Core Methods
    # ------------------------------------------------------------------

    def complete(
        self,
        input: str | list,
        response_model: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Callable]] = None,
    ):
        """
        Send a synchronous completion request to the LLM.
        """
        try:
            input = self._inject_runtime_instructions(input, response_model)

            payload = (
                getattr(self, "payload", {}).copy()
                if isinstance(getattr(self, "payload", {}), dict)
                else {}
            )
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

    async def async_complete(
        self,
        input: str | list,
        response_model: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Callable]] = None,
    ):
        """
        Send an asynchronous completion request to the LLM.
        """
        try:
            input = self._inject_runtime_instructions(input, response_model)

            payload = (
                getattr(self, "payload", {}).copy()
                if isinstance(getattr(self, "payload", {}), dict)
                else {}
            )
            payload["model"] = self.model
            if isinstance(input, str):
                if "messages" not in payload or not payload["messages"]:
                    payload["messages"] = [{"role": "user", "content": ""}]
                payload["messages"][-1]["content"] = input

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url, headers=self.headers, json=payload
                )
                if self.verbose:
                    print(response)
                return response
        except Exception as e:
            import traceback

            traceback.print_exc()

    def _format_tools(self, tools: List[Callable]) -> Any:
        """To be implemented by subclasses to map tools to provider-specific schemas."""
        return None

    def get_text_response(self, response: Any) -> str:
        """To be implemented by subclasses."""
        return ""

import pytest
from unittest.mock import MagicMock, patch
from pydantic import BaseModel
from typing import Optional, Type, Any
from maticlib.client.classes.base_client import BaseLLMClient
from maticlib.client.classes.client_output_model import LLMResponseBase


# Mock response class that inherits from LLMResponseBase
class MockResponse(LLMResponseBase):
    content: str
    status_code: int = 200


# Minimal concrete implementation of BaseLLMClient for testing
class ConcreteClient(BaseLLMClient):
    def __init__(self, return_raw=False):
        self.return_raw = return_raw
        self.verbose = False

    def complete(self, input, response_model=None):
        # 1. Inject instructions
        modified_input = self._inject_runtime_instructions(input, response_model)

        # 2. Simulate LLM response
        if response_model:
            content = '{"name": "Test User", "age": 50}'
        else:
            content = "Hello world"

        response = MockResponse(content=content, model="mock-model")

        # 3. Apply parsing
        self._apply_response_model(response, response_model)
        return response, modified_input

    def get_text_response(self, response):
        return response.content

    async def async_complete(self, input, response_model=None):
        return self.complete(input, response_model)


class TestModel(BaseModel):
    name: str
    age: int


def test_inject_runtime_instructions():
    client = ConcreteClient()
    input_text = "Who is the user?"

    # Without model
    res1, mod1 = client.complete(input_text)
    assert mod1 == input_text

    # With model
    res2, mod2 = client.complete(input_text, response_model=TestModel)
    assert input_text in mod2
    assert "JSON object matching this schema" in mod2


def test_apply_response_model_success():
    client = ConcreteClient()
    response, _ = client.complete("query", response_model=TestModel)

    assert response.parsed_output is not None
    assert isinstance(response.parsed_output, TestModel)
    assert response.parsed_output.name == "Test User"
    assert response.parsed_output.age == 50


def test_apply_response_model_failure():
    client = ConcreteClient()

    # Simulate a response that doesn't match the model
    with patch.object(ConcreteClient, "get_text_response", return_value="Invalid JSON"):
        response = MockResponse(content="Invalid JSON", model="mock-model")
        client._apply_response_model(response, TestModel)

        assert response.parsed_output is None
        # Should not raise exception, just log/print warning in our current implementation

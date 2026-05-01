"""
Tests for OpenAIClient
========================
Covers:
  - Mocked unit tests (no API key required)   → run with: pytest -v
  - Real API integration tests                 → run with: pytest -v -m real_api
    Requires OPENAI_API_KEY set in .env or environment.
"""

import os
import pytest
from maticlib.llm.openai.client import OpenAIClient
from maticlib.llm.openai.openai_classes import OpenAIResponse
from maticlib.messages import HumanMessage, SystemMessage, AIMessage
from maticlib.tools import tool


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def openai_client():
    """Returns an OpenAIClient configured with a fake key and verbose=False."""
    return OpenAIClient(
        model="gpt-4o-mini",
        api_key="test-key",
        verbose=False,
    )


# Minimal realistic response from the OpenAI Responses API
MOCK_RESPONSE = {
    "id": "resp_abc123",
    "object": "response",
    "created_at": 1714000000,
    "status": "completed",
    "model": "gpt-4o-mini-2024-07-18",
    "output": [
        {
            "id": "msg_001",
            "type": "message",
            "status": "completed",
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": "Hello! How can I help you today?",
                    "annotations": [],
                }
            ],
        }
    ],
    "usage": {
        "input_tokens": 10,
        "output_tokens": 9,
        "total_tokens": 19,
        "output_tokens_details": {"reasoning_tokens": 0},
        "input_tokens_details": {"cached_tokens": 0, "audio_tokens": 0},
    },
}


# Realistic response containing a tool call
MOCK_TOOL_RESPONSE = {
    "id": "resp_tool123",
    "object": "response",
    "created_at": 1714000000,
    "status": "completed",
    "model": "gpt-4o-mini",
    "output": [
        {
            "id": "call_abc",
            "type": "call_tool",
            "status": "completed",
            "call_tool": {
                "name": "get_weather",
                "arguments": {"location": "Paris"}
            }
        }
    ],
    "usage": {
        "input_tokens": 15,
        "output_tokens": 5,
        "total_tokens": 20
    }
}


# ---------------------------------------------------------------------------
# Unit tests — message formatting
# ---------------------------------------------------------------------------

class TestFormatInput:
    """Tests for OpenAIClient._format_input."""

    def test_string_passthrough(self, openai_client):
        """Plain strings should be returned as-is."""
        result = openai_client._format_input("Hello!")
        assert result == "Hello!"

    def test_human_message_object(self, openai_client):
        """HumanMessage objects should map to role=user."""
        result = openai_client._format_input([HumanMessage(content="Hi")])
        assert result == [{"role": "user", "content": "Hi"}]

    def test_system_message_object(self, openai_client):
        """SystemMessage objects should map to role=developer."""
        result = openai_client._format_input([SystemMessage(content="Be helpful")])
        assert result == [{"role": "developer", "content": "Be helpful"}]

    def test_ai_message_object(self, openai_client):
        """AIMessage objects should map to role=assistant."""
        result = openai_client._format_input([AIMessage(content="Sure!")])
        assert result == [{"role": "assistant", "content": "Sure!"}]

    def test_dict_role_alias(self, openai_client):
        """Dict messages with role='human' should be normalised to 'user'."""
        result = openai_client._format_input([{"role": "human", "content": "Hey"}])
        assert result[0]["role"] == "user"

    def test_dict_missing_role_raises(self, openai_client):
        with pytest.raises(ValueError, match="role"):
            openai_client._format_input([{"content": "No role!"}])


# ---------------------------------------------------------------------------
# Unit tests — response model
# ---------------------------------------------------------------------------

class TestOpenAIResponse:
    """Tests for the OpenAIResponse Pydantic model."""

    def test_content_extraction(self):
        """content field should be populated from output_text parts."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert resp.content == "Hello! How can I help you today?"

    def test_content_parts(self):
        """content_parts should contain one ContentPart."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert resp.content_parts is not None
        assert len(resp.content_parts) == 1
        assert resp.content_parts[0].text == "Hello! How can I help you today?"

    def test_token_mapping(self):
        """Token fields should be mapped from usage.*_tokens."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert resp.prompt_tokens == 10
        assert resp.completion_tokens == 9
        assert resp.total_tokens == 19

    def test_response_id(self):
        """response_id should equal the top-level id."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert resp.response_id == "resp_abc123"

    def test_timestamp(self):
        """timestamp computed field should be a datetime."""
        from datetime import datetime
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert isinstance(resp.timestamp, datetime)

    def test_reasoning_tokens_zero(self):
        """reasoning_tokens should be 0 for standard GPT models."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert resp.reasoning_tokens == 0

    def test_cached_tokens_zero(self):
        """cached_tokens should be 0 when there is no cache hit."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert resp.cached_tokens == 0

    def test_raw_response_stored(self):
        """raw_response should be a non-empty dict."""
        resp = OpenAIResponse(**MOCK_RESPONSE)
        assert isinstance(resp.raw_response, dict)
        assert "id" in resp.raw_response

    def test_tool_call_extraction(self):
        """tool_calls should be extracted from 'call_tool' output items."""
        resp = OpenAIResponse(**MOCK_TOOL_RESPONSE)
        assert resp.tool_calls is not None
        assert len(resp.tool_calls) == 1
        assert resp.tool_calls[0]["function"]["name"] == "get_weather"
        assert resp.tool_calls[0]["function"]["arguments"] == {"location": "Paris"}


# ---------------------------------------------------------------------------
# Unit tests — synchronous complete (mocked HTTP)
# ---------------------------------------------------------------------------

class TestComplete:
    """Tests for OpenAIClient.complete using httpx_mock."""

    def test_complete_string_input(self, openai_client, httpx_mock):
        httpx_mock.add_response(json=MOCK_RESPONSE, status_code=200)
        response = openai_client.complete("Hello")
        assert isinstance(response, OpenAIResponse)
        assert response.content == "Hello! How can I help you today?"

    def test_get_text_response_model(self, openai_client, httpx_mock):
        httpx_mock.add_response(json=MOCK_RESPONSE, status_code=200)
        response = openai_client.complete("Hello")
        text = openai_client.get_text_response(response)
        assert text == "Hello! How can I help you today?"

    def test_get_text_response_raw_dict(self, openai_client):
        """get_text_response should also work on a raw dict."""
        text = openai_client.get_text_response(MOCK_RESPONSE)
        assert text == "Hello! How can I help you today?"

    def test_return_raw_flag(self, openai_client, httpx_mock):
        """When return_raw=True, complete should return a dict."""
        openai_client.return_raw = True
        httpx_mock.add_response(json=MOCK_RESPONSE, status_code=200)
        response = openai_client.complete("Hello")
        assert isinstance(response, dict)
        assert response["id"] == "resp_abc123"
        openai_client.return_raw = False  # reset

    def test_system_instruct_adds_instructions_key(self, openai_client, httpx_mock):
        """When system_instruct is set, payload should include 'instructions'."""
        openai_client.system_instruct = "You are a helpful assistant."
        httpx_mock.add_response(json=MOCK_RESPONSE, status_code=200)

        # Inspect the actual request payload sent
        openai_client.complete("Hello")
        request = httpx_mock.get_requests()[0]
        import json
        payload = json.loads(request.content)
        assert payload.get("instructions") == "You are a helpful assistant."
        openai_client.system_instruct = None  # reset

    def test_list_input(self, openai_client, httpx_mock):
        """complete should accept a list of HumanMessages."""
        httpx_mock.add_response(json=MOCK_RESPONSE, status_code=200)
        response = openai_client.complete([HumanMessage(content="Hello")])
        assert isinstance(response, OpenAIResponse)

    def test_complete_with_tools_payload(self, openai_client, httpx_mock):
        """When tools are provided, they should be in the request payload."""
        @tool
        def my_test_tool(x: int):
            """Test tool."""
            return x

        httpx_mock.add_response(json=MOCK_TOOL_RESPONSE, status_code=200)
        response = openai_client.complete("Use the tool", tools=[my_test_tool])
        
        request = httpx_mock.get_requests()[0]
        import json
        payload = json.loads(request.content)
        
        assert "tools" in payload
        assert payload["tools"][0]["type"] == "function"
        assert payload["tools"][0]["function"]["name"] == "my_test_tool"
        assert response.tool_calls[0]["function"]["name"] == "get_weather"


# ---------------------------------------------------------------------------
# Unit tests — async complete (mocked HTTP)
# ---------------------------------------------------------------------------

class TestAsyncComplete:
    """Tests for OpenAIClient.async_complete using httpx_mock."""

    @pytest.mark.asyncio
    async def test_async_complete_string_input(self, openai_client, httpx_mock):
        httpx_mock.add_response(json=MOCK_RESPONSE, status_code=200)
        response = await openai_client.async_complete("Hello async")
        assert isinstance(response, OpenAIResponse)
        assert openai_client.get_text_response(response) == "Hello! How can I help you today?"


# ---------------------------------------------------------------------------
# Real API tests (skipped unless OPENAI_API_KEY is set)
# ---------------------------------------------------------------------------

@pytest.mark.real_api
def test_openai_real_api_sync():
    """
    Integration test — calls the real OpenAI API synchronously.

    Run with: pytest -v -m real_api
    Requires OPENAI_API_KEY in environment or .env file.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    client = OpenAIClient(model="gpt-4o-mini", verbose=True)
    response = client.complete("Say hello in one sentence.")
    text = client.get_text_response(response)
    assert len(text) > 0


@pytest.mark.real_api
@pytest.mark.asyncio
async def test_openai_real_api_async():
    """
    Integration test — calls the real OpenAI API asynchronously.

    Run with: pytest -v -m real_api
    Requires OPENAI_API_KEY in environment or .env file.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    client = OpenAIClient(model="gpt-4o-mini", verbose=True)
    response = await client.async_complete("Say hello in one sentence.")
    text = client.get_text_response(response)
    assert len(text) > 0

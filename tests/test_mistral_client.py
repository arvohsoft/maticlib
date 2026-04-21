import pytest
import httpx
import os
from maticlib.llm.mistral.client import MistralClient
from maticlib.messages import HumanMessage, SystemMessage
from maticlib.tools import tool

@pytest.fixture
def mistral_client():
    return MistralClient(
        model="mistral-tiny",
        api_key="test-key",
        verbose=False
    )

# Mock response with tool call
MOCK_MISTRAL_TOOL_RESPONSE = {
    "id": "cmpl-tool...",
    "object": "chat.completion",
    "created": 1702256327,
    "model": "mistral-tiny",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "call_123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "arguments": "{\"location\": \"Paris\"}"
                        }
                    }
                ]
            },
            "finish_reason": "tool_calls"
        }
    ],
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 10,
        "total_tokens": 30
    }
}

def test_mistral_client_format_messages(mistral_client):
    # Test string input
    msgs = mistral_client._format_messages("Hello")
    assert msgs == [{"role": "user", "content": "Hello"}]
    
    # Test HumanMessage
    msgs = mistral_client._format_messages([HumanMessage(content="Hi")])
    assert msgs == [{"role": "user", "content": "Hi"}]

def test_mistral_client_complete(mistral_client, httpx_mock):
    # Mock response
    mock_response = {
        "id": "cmpl-e5cc...",
        "object": "chat.completion",
        "created": 1702256327,
        "model": "mistral-tiny",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you?"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 15,
            "completion_tokens": 8,
            "total_tokens": 23
        }
    }
    httpx_mock.add_response(json=mock_response, status_code=200)
    
    response = mistral_client.complete("Hello")
    assert response.model == "mistral-tiny"
    assert mistral_client.get_text_response(response) == "Hello! How can I help you?"

def test_mistral_client_tools_payload(mistral_client, httpx_mock):
    @tool
    def search(query: str):
        """Search tool."""
        return f"Results for {query}"

    httpx_mock.add_response(json=MOCK_MISTRAL_TOOL_RESPONSE, status_code=200)
    response = mistral_client.complete("Search for moon", tools=[search])
    
    request = httpx_mock.get_requests()[0]
    import json
    payload = json.loads(request.content)
    
    assert "tools" in payload
    assert payload["tools"][0]["type"] == "function"
    assert payload["tools"][0]["function"]["name"] == "search"
    
    assert response.tool_calls is not None
    assert response.tool_calls[0]["id"] == "call_123"
    assert response.tool_calls[0]["function"]["name"] == "get_weather"

@pytest.mark.asyncio
async def test_mistral_client_async_complete(mistral_client, httpx_mock):
    mock_response = {
        "id": "cmpl-async...",
        "object": "chat.completion",
        "created": 1702256327,
        "model": "mistral-tiny",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Async Hello!"
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 5,
            "total_tokens": 10
        }
    }
    httpx_mock.add_response(json=mock_response, status_code=200)
    
    response = await mistral_client.async_complete("Hello async")
    assert mistral_client.get_text_response(response) == "Async Hello!"

@pytest.mark.real_api
def test_mistral_client_real_api():
    if not os.getenv("MISTRAL_API_KEY"):
        pytest.skip("MISTRAL_API_KEY not set")
    
    client = MistralClient(verbose=True)
    response = client.complete("Say hello!")
    text = client.get_text_response(response)
    assert len(text) > 0

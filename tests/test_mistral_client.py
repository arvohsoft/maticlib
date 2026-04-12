import pytest
import httpx
import os
from maticlib.llm.mistral.client import MistralClient
from maticlib.messages import HumanMessage, SystemMessage

@pytest.fixture
def mistral_client():
    return MistralClient(
        model="mistral-tiny",
        api_key="test-key",
        verbose=False
    )

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

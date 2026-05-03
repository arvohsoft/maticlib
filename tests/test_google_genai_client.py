import pytest
import os
from maticlib.llm.google_genai.client import GoogleGenAIClient
from maticlib.messages import HumanMessage
from maticlib.tools import tool


@pytest.fixture
def gemini_client():
    return GoogleGenAIClient(
        model="gemini-2.5-flash-lite", api_key="test-key", verbose=False
    )


# Mock response with tool call
MOCK_GEMINI_TOOL_RESPONSE = {
    "responseId": "test-id",
    "modelVersion": "gemini-2.5-flash-lite",
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "functionCall": {
                            "name": "get_weather",
                            "args": {"location": "Paris"},
                        }
                    }
                ],
                "role": "model",
            },
            "finishReason": "STOP",
            "index": 0,
        }
    ],
    "usageMetadata": {
        "promptTokenCount": 10,
        "candidatesTokenCount": 5,
        "totalTokenCount": 15,
    },
}


def test_gemini_client_format_messages(gemini_client):
    msgs = gemini_client._format_messages("Hello")
    assert msgs == [{"parts": [{"text": "Hello"}]}]

    msgs = gemini_client._format_messages([HumanMessage(content="Hi")])
    assert msgs == [{"role": "user", "parts": [{"text": "Hi"}]}]


def test_gemini_client_complete(gemini_client, httpx_mock):
    mock_response = {
        "responseId": "test-id",
        "modelVersion": "gemini-1.5-flash",
        "candidates": [
            {
                "content": {"parts": [{"text": "Hello from Gemini!"}], "role": "model"},
                "finishReason": "STOP",
                "index": 0,
            }
        ],
        "usageMetadata": {
            "promptTokenCount": 5,
            "candidatesTokenCount": 5,
            "totalTokenCount": 10,
        },
    }
    httpx_mock.add_response(json=mock_response, status_code=200)

    response = gemini_client.complete("Hello")
    assert gemini_client.get_text_response(response) == "Hello from Gemini!"


def test_gemini_client_tools_payload(gemini_client, httpx_mock):
    @tool
    def search(query: str):
        """Search tool."""
        return f"Results for {query}"

    httpx_mock.add_response(json=MOCK_GEMINI_TOOL_RESPONSE, status_code=200)
    response = gemini_client.complete("Search for moon", tools=[search])

    request = httpx_mock.get_requests()[0]
    import json

    payload = json.loads(request.content)

    assert "tools" in payload
    assert "function_declarations" in payload["tools"][0]
    assert payload["tools"][0]["function_declarations"][0]["name"] == "search"

    assert response.tool_calls is not None
    assert response.tool_calls[0]["function"]["name"] == "get_weather"
    assert response.tool_calls[0]["function"]["arguments"] == {"location": "Paris"}


@pytest.mark.asyncio
async def test_gemini_client_async_complete(gemini_client, httpx_mock):
    mock_response = {
        "responseId": "test-id",
        "modelVersion": "gemini-1.5-flash",
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Async Hello from Gemini!"}],
                    "role": "model",
                },
                "finishReason": "STOP",
                "index": 0,
            }
        ],
    }
    httpx_mock.add_response(json=mock_response, status_code=200)

    response = await gemini_client.async_complete("Hello async")
    assert gemini_client.get_text_response(response) == "Async Hello from Gemini!"


@pytest.mark.real_api
@pytest.mark.asyncio
async def test_gemini_client_real_api_async():
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GOOGLE_API_KEY not set")

    client = GoogleGenAIClient(verbose=True)
    response = await client.async_complete("Say hello asynchronously!")
    text = client.get_text_response(response)
    assert len(text) > 0

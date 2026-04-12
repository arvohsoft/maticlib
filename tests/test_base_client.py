import pytest
import httpx
from maticlib.client.classes.base_client import BaseLLMClient

@pytest.fixture
def base_client():
    return BaseLLMClient(
        inference_url="https://api.example.com/v1/chat",
        header={"Authorization": "Bearer token"},
        model="test-model",
        payload={"messages": [{"role": "system", "content": "You are a test."}]},
        verbose=False
    )

def test_base_client_init(base_client):
    assert base_client.url == "https://api.example.com/v1/chat"
    assert base_client.model == "test-model"

def test_base_client_complete(base_client, httpx_mock):
    httpx_mock.add_response(json={"result": "success"}, status_code=200)
    
    response = base_client.complete("Hello")
    assert response.status_code == 200
    assert response.json() == {"result": "success"}

@pytest.mark.asyncio
async def test_base_client_async_complete(base_client, httpx_mock):
    httpx_mock.add_response(json={"result": "async_success"}, status_code=200)
    
    response = await base_client.async_complete("Hello async")
    assert response.status_code == 200
    assert response.json() == {"result": "async_success"}

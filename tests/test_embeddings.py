import pytest
import os
from maticlib.embeddings import OpenAIEmbeddings, GoogleGenAIEmbeddings, MistralEmbeddings

@pytest.fixture
def mock_env_keys(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-test-key")
    monkeypatch.setenv("MISTRAL_API_KEY", "mistral-test-key")

def test_openai_embeddings_init(mock_env_keys):
    client = OpenAIEmbeddings()
    assert client.model == "text-embedding-3-small"
    assert client.headers["Authorization"] == "Bearer sk-test-key"

def test_google_embeddings_init(mock_env_keys):
    client = GoogleGenAIEmbeddings()
    assert client.model == "models/gemini-embedding-001"
    assert client.headers["x-goog-api-key"] == "google-test-key"

def test_mistral_embeddings_init(mock_env_keys):
    client = MistralEmbeddings()
    assert client.model == "mistral-embed"
    assert client.headers["Authorization"] == "Bearer mistral-test-key"

def test_openai_embed_documents(httpx_mock, mock_env_keys):
    client = OpenAIEmbeddings(verbose=False)
    
    mock_response = {
        "data": [
            {"embedding": [0.1, 0.2], "index": 0},
            {"embedding": [0.3, 0.4], "index": 1}
        ],
        "usage": {"prompt_tokens": 5}
    }
    httpx_mock.add_response(json=mock_response)
    
    res = client.embed_documents(["hello", "world"])
    assert res.vectors == [[0.1, 0.2], [0.3, 0.4]]
    assert res.prompt_tokens == 5

def test_google_embed_documents(httpx_mock, mock_env_keys):
    client = GoogleGenAIEmbeddings(verbose=False)
    
    mock_response = {
        "embeddings": [
            {"values": [0.1, 0.2]},
            {"values": [0.3, 0.4]}
        ],
        "usageMetadata": {"promptTokenCount": 7}
    }
    httpx_mock.add_response(json=mock_response)
    
    res = client.embed_documents(["hello", "world"])
    assert res.vectors == [[0.1, 0.2], [0.3, 0.4]]
    assert res.prompt_tokens == 7

def test_mistral_embed_documents(httpx_mock, mock_env_keys):
    client = MistralEmbeddings(verbose=False)
    
    mock_response = {
        "data": [
            {"embedding": [0.1, 0.2], "index": 0},
            {"embedding": [0.3, 0.4], "index": 1}
        ],
        "usage": {"prompt_tokens": 10}
    }
    httpx_mock.add_response(json=mock_response)
    
    res = client.embed_documents(["hello", "world"])
    assert res.vectors == [[0.1, 0.2], [0.3, 0.4]]
    assert res.prompt_tokens == 10

import pytest
import os
from maticlib.embeddings import OpenAIEmbeddings, GoogleGenAIEmbeddings, MistralEmbeddings

@pytest.fixture
def mock_env_keys():
    os.environ["OPENAI_API_KEY"] = "sk-test-key"
    os.environ["GOOGLE_API_KEY"] = "google-test-key"
    os.environ["MISTRAL_API_KEY"] = "mistral-test-key"

def test_openai_embeddings_init(mock_env_keys):
    client = OpenAIEmbeddings()
    assert client.model == "text-embedding-3-small"
    assert client.headers["Authorization"] == "Bearer sk-test-key"

def test_google_embeddings_init(mock_env_keys):
    client = GoogleGenAIEmbeddings()
    assert client.model == "models/text-embedding-004"
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
        ]
    }
    httpx_mock.add_response(json=mock_response)
    
    embeddings = client.embed_documents(["hello", "world"])
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]

def test_google_embed_documents(httpx_mock, mock_env_keys):
    client = GoogleGenAIEmbeddings(verbose=False)
    
    mock_response = {
        "embeddings": [
            {"values": [0.1, 0.2]},
            {"values": [0.3, 0.4]}
        ]
    }
    httpx_mock.add_response(json=mock_response)
    
    embeddings = client.embed_documents(["hello", "world"])
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]

def test_mistral_embed_documents(httpx_mock, mock_env_keys):
    client = MistralEmbeddings(verbose=False)
    
    mock_response = {
        "data": [
            {"embedding": [0.1, 0.2], "index": 0},
            {"embedding": [0.3, 0.4], "index": 1}
        ]
    }
    httpx_mock.add_response(json=mock_response)
    
    embeddings = client.embed_documents(["hello", "world"])
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]

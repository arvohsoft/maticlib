# :material-vector-arrange-below: Embeddings (`maticlib.embeddings`)

The Embeddings module provides a unified interface for generating high-dimensional vector representations of text across multiple providers.

### **Unified Interface**

All embedding clients share two core methods:
- **`embed_query(text)`**: Returns a single vector (List[float]) for search queries.
- **`embed_documents(texts)`**: Returns a list of vectors (List[List[float]]) optimized for indexing large document sets.

### **Example Usage**

```python
from maticlib.embeddings import OpenAIEmbeddings, GoogleGenAIEmbeddings

# 1. Initialize (automatically picks up API keys from env)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2. Embed a single query
query_vector = embeddings.embed_query("How do I use embeddings?")

# 3. Embed a batch of documents
doc_vectors = embeddings.embed_documents([
    "Embeddings are vector representations of text.",
    "They are useful for semantic search and RAG."
])

print(f"Vector Dimensions: {len(query_vector)}")
```

### **Supported Providers**

| Provider | Client Class | Default Model |
| :--- | :--- | :--- |
| **OpenAI** | `OpenAIEmbeddings` | `text-embedding-3-small` |
| **Google Gemini** | `GoogleGenAIEmbeddings` | `gemini-embedding-001` |
| **Mistral AI** | `MistralEmbeddings` | `mistral-embed` |

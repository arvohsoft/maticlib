# :material-database: Vector Stores (`maticlib.vectorstores`)

Manage and query high-dimensional embeddings across different backend engines.

### **Supported Engines**
- **`InMemoryVectorIndex`**: Great for quick, lightweight local testing via Numpy.
- **`ChromaVectorIndex`**: Ephemeral or persistent ChromaDB instances.
- **`MilvusVectorIndex`**: Scalable PyMilvus (Lite or Server modes).
- **`PineconeVectorIndex`**: Connects directly to Pinecone Cloud.
- **`QdrantVectorIndex`**: Uses Qdrant Cloud or local instances.
- **`SchemaVectorIndex`**: A wrapper explicitly for storing database schemas (DDLs) for Text2SQL workflows.

```python
from maticlib.vectorstores.chroma import ChromaVectorIndex
from maticlib.embeddings.openai import OpenAIEmbeddings

vector_index = ChromaVectorIndex(
    embeddings=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)
results = vector_index.similarity_search("How do I fix this error?", k=3)
```

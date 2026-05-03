# :material-pipe: High-Level Pipelines (`maticlib.pipelines`)

The ultimate orchestration layer tying everything together.

### **RAGPipeline**
A complete wrapper handling Query Transformation, Hybrid Keyword Retrieval, and Generation.

```python
from maticlib.pipelines.rag_pipeline import RAGPipeline

pipeline = RAGPipeline(
    llm_client=client,
    vector_index=vector_index,
    use_hybrid=True,
    use_query_transform=True
)
answer = pipeline.generate("What is Maticlib?")
```

### **Text2SQLPipeline**
A complete wrapper handling Schema loading, LLM SQL Generation, SQL Injection Guarding, and Execution.

```python
from maticlib.pipelines.text2sql_pipeline import Text2SQLPipeline

pipeline = Text2SQLPipeline(
    llm_client=client,
    schema_loader=schema_loader,
    executor=executor,
    connection_string="sqlite:///data.db"
)
columns, rows = pipeline.execute("Show me the top 5 users by revenue")
```

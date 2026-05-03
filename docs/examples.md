# Examples Gallery

Check out these runnable examples to learn how to use Maticlib for different use cases. You can find all these scripts in the `examples/` directory of the repository.

---

## :material-chat-outline: Basic Chat & Multi-Provider
Demonstrates how to initialize and use LLM clients from different providers.

- **[Basic Sync Chat](https://github.com/arvohsoft/maticlib/blob/main/examples/01_basic_chat.py)**: A simple script to get text responses from OpenAI, Mistral, and Gemini.
- **[Focused OpenAI Example](https://github.com/arvohsoft/maticlib/blob/main/examples/openai_only.py)**: Detailed usage of OpenAI-specific features like reasoning tokens.
- **[Async Concurrent Chat](https://github.com/arvohsoft/maticlib/blob/main/examples/02_async_chat.py)**: Sending requests to multiple models at the same time using `asyncio.gather`.

---

## :material-sitemap-outline: Graph Workflows
Learn how to build intelligent agents using the `MaticGraph` engine.

- **[Sequential Graph](https://github.com/arvohsoft/maticlib/blob/main/examples/03_sequential_graph.py)**: A basic A → B → C pipeline.
- **[Conditional Routing](https://github.com/arvohsoft/maticlib/blob/main/examples/04_conditional_reporting.py)**: Branching logic based on model outputs (e.g., sentiment analysis).
- **[Parallel Node Execution](https://github.com/arvohsoft/maticlib/blob/main/examples/05_parallel_execution.py)**: Running multiple independent analysis nodes in parallel for maximum performance.

---

## :material-cog-outline: Structured Output & Parsing
- **[Pydantic Response Parsing](https://github.com/arvohsoft/maticlib/blob/main/examples/08_pydantic_parsing.py)**: Force models to generate validated JSON that maps directly to your Pydantic schemas.
- **[Typed Graph State](https://github.com/arvohsoft/maticlib/blob/main/examples/06_typed_state.py)**: Using Pydantic models to enforce strict state schemas throughout your graph workflows.

---

## :material-hammer-wrench: Native Tool Calling
- **[Tool Definition & Usage](https://github.com/arvohsoft/maticlib/blob/main/examples/09_tool_calling.py)**: Use the `@tool` decorator to let LLMs call your Python functions directly.

## :material-database-search: RAG & Text2SQL
- **[Context Engineering Basics](https://github.com/arvohsoft/maticlib/blob/main/examples/11_chunkers_and_loaders.py)**: How to extract text from PDFs, Webpages, and TXTs, and chunk them correctly.
- **[Secure Text2SQL Engine](https://github.com/arvohsoft/maticlib/blob/main/examples/12_text2sql_basics.py)**: Auto-reflecting databases and generating strictly validated, injection-proof SQL queries.
- **[RAG Pipeline & In-Memory Vector Store](https://github.com/arvohsoft/maticlib/blob/main/examples/14_vectorstores_and_pipelines.py)**: A complete end-to-end RAG pipeline using `InMemoryVectorIndex` and Query Transformers.
- **[Chroma Vector Store](https://github.com/arvohsoft/maticlib/blob/main/examples/15_chroma_vectorstore.py)**: Using the `ChromaVectorIndex` for persistent local embedding storage.
- **[Milvus Vector Store](https://github.com/arvohsoft/maticlib/blob/main/examples/16_milvus_vectorstore.py)**: Using the `MilvusVectorIndex` (Lite mode) for scalable vector search.
- **[Milvus Server Vector Store](https://github.com/arvohsoft/maticlib/blob/main/examples/17_milvus_server_vectorstore.py)**: Connecting to a standalone Milvus Server at `http://localhost:19530`.

---

## :material-eye-outline: Observability & Resilience
- **[Traces, Retry & Memory](https://github.com/arvohsoft/maticlib/blob/main/examples/13_prompts_and_observability.py)**: Using the Prompt Registry, rolling window memory buffers, handling external API failures with exponential backoff, and tracing exact token usages via Callbacks.
- **[Formatting & Evaluation](https://github.com/arvohsoft/maticlib/blob/main/examples/18_evaluation_and_formatting.py)**: Converting raw SQL results into Markdown tables and computing context relevance and answer accuracy scores without external dependencies.

---

## Running the Examples

1. **Set up your environment**:
   Make sure you have your API keys in a `.env` file.

2. **Execute a script**:
   ```bash
   # From the project root
   python examples/01_basic_chat.py
   ```

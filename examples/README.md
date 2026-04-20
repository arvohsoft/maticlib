# MaticLib Examples

Welcome to the `maticlib` examples gallery! These scripts demonstrate how to use the core features of the library, from basic LLM interactions to complex graph-based workflows.

## Prerequisites

Before running the examples, ensure you have:
1.  **Installed dependencies**: `pip install -e .`
2.  **Set up API Keys**: Copy `.env.example` to `.env` and fill in your keys for OpenAI, Mistral, and Google Gemini.

## 🚀 The Examples

### 1. LLM Clients
*   **[01_basic_chat.py](./01_basic_chat.py)**: The "Hello World" of `maticlib`. Shows how to use synchronous clients for OpenAI, Mistral, and Gemini.
*   **[02_async_chat.py](./02_async_chat.py)**: Shows how to send multiple model requests concurrently using Python's `asyncio` for maximum efficiency.

### 2. Graph Workflows
*   **[03_sequential_graph.py](./03_sequential_graph.py)**: A basic linear workflow where data flows through two processing nodes.
*   **[04_conditional_reporting.py](./04_conditional_reporting.py)**: Demonstrates branching logic—routing execution to different nodes based on the results of previous ones (e.g., sentiment analysis).
*   **[05_parallel_execution.py](./05_parallel_execution.py)**: Shows how to trigger multiple tasks simultaneously using the `parallel_group` feature and join their results.

### 3. Advanced State Management
*   **[06_typed_state.py](./06_typed_state.py)**: For production use cases, this shows how to use Pydantic `BaseModel` as a graph state to get type-safety, validation, and IDE auto-completion.

---

## How to Run

To run an example, execute it from the root directory of the project:

```bash
python examples/03_sequential_graph.py
```

*Note: For examples 01 and 02, you will need active API keys in your `.env` file.*

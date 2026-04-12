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

## :material-cog-outline: Advanced State Management
- **[Typed Pydantic State](https://github.com/arvohsoft/maticlib/blob/main/examples/06_typed_state.py)**: Using Pydantic models to enforce strict state schemas throughout your graph workflows.

---

## Running the Examples

1. **Set up your environment**:
   Make sure you have your API keys in a `.env` file.

2. **Execute a script**:
   ```bash
   # From the project root
   python examples/01_basic_chat.py
   ```

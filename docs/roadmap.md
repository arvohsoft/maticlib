# Roadmap

Maticlib is actively developed. Below is the current progress and planned features for the library.

## Core Library
- [x] Google Gemini integration
- [x] Mistral AI integration
- [x] OpenAI Responses API integration
- [x] Graph-based workflow engine
- [x] Parallel node execution
- [x] Automated documentation system
- [x] Native Tool/Function calling system
- [x] **API Reference Architecture**: Standardized Google-style docstrings with table rendering
- [x] **Documentation Modularization**: Decoupled, component-based Modules & API guide
- [ ] Anthropic Claude integration
- [ ] Ollama (Local LLM) integration
- [ ] Streaming support for all providers

## Advanced Features
- [x] Embeddings support (OpenAI, Google, Mistral)
- [x] **Context Engineering**: Advanced Chunkers & Document Loaders
- [x] **Text2SQL Engine**: Schema Reflection, Transpilation, and Validation Guards
- [x] **Vector Stores**: Native integrations (Chroma, Milvus, Qdrant, Pinecone)
- [x] **Full Telemetry & Observability**: Pipeline Traces and Logging Callbacks
- [x] **Resilience**: Exponential Backoff and Retry Policies
- [x] **Memory Management**: Rolling Window and Conversation Buffers
- [x] **Formatting Utilities**: Converting execution outputs to aligned Markdown tables
- [x] **RAG & Text2SQL Evaluation**: Fuzzy heuristics & pluggable LLM metrics for relevance and accuracy
- [ ] **Agent Tooling**: Built-in tools for Playwright, Selenium, Code Execution, and Bash/CLI scripting.
- [ ] **MCP Support**: Tools to both host MCP servers and consume MCP clients.
- [ ] **Agent Integration**: Higher-level Agent abstractions for complex task decomposition.
- [ ] Multi-agent collaboration protocols
- [ ] Workflow persistence & checkpointing
- [x] Detailed Token Usage Tracking

## Deployment & Ecosystem
- [ ] **FastAPI Integration**: One-line utility to expose any `MaticGraph` or Agent as a streaming REST API.
- [ ] **MaticUI**: A professional-grade interface for testing and production-ready agent interactions (with future support for authentication).

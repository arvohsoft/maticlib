# Changelog

All notable changes to maticlib will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.9] - 2026-05-01

### Added
- **Embeddings Token Tracking & Metadata**: Changed `embed_query()` and `embed_documents()` return types to Pydantic objects (`EmbedQueryResponse` and `EmbedDocumentsResponse`).
- Added token tracking (`prompt_tokens`, `total_tokens`), model info, and raw response extraction inside the new Pydantic response models for `OpenAIEmbeddings`, `GoogleGenAIEmbeddings`, and `MistralEmbeddings`.

## [0.1.8] - 2026-04-29

### Added
- **RAG & Context Engineering (Phase 1)**
  - Implemented a unified `BaseEmbeddings` interface for generating high-dimensional vector representations.
  - Added `OpenAIEmbeddings` supporting `text-embedding-3` models with dimensionality controls.
  - Added `GoogleGenAIEmbeddings` supporting `gemini-embedding-001` with task-type optimization.
  - Added `MistralEmbeddings` supporting `mistral-embed`.
  - Added synchronous `embed_query()` and `embed_documents()` methods to all clients.
  - Created `examples/10_rag_basics.py` to demonstrate unified usage.

## [0.1.7] - 2026-04-21

- **Native Tool Calling (Function Calling)**
  - Implemented `@tool` decorator that automatically generates JSON schemas from Python function signatures and docstrings.
  - Added native tool calling support to `OpenAIClient` (v1/responses API).
  - Added native tool calling support to `GoogleGenAIClient` (Gemini API).
  - Added native tool calling support to `MistralClient` (Chat Completions API).
  - Standardized `tool_calls` extraction across all providers into the `LLMResponseBase`.
  - New `examples/09_tool_calling.py` demonstrating multi-provider tool usage.

## [0.1.6] - 2026-04-17
 
### Added
- **Response Parser System**
  - Standardized interface for extracting structured data from LLM responses.
  - Implemented `PydanticResponseParser` for automatic validation against Pydantic models.
  - Implemented `JSONResponseParser` and `XMLResponseParser` for specialized data extraction.
  - Integrated `response_model` parameter directly into all LLM client `complete()` methods.
 
### Changed
- **LLM Clients**
  - Updated default Google Gemini model to `gemini-2.5-lite`.
  - Refactored API key detection to run at instantiation rather than import, improving compatibility with `.env` files.
- **Documentation Overhaul**
  - Reorganized site navigation: introduced a comprehensive, code-first "Modules" guide and expanded API Reference.
  - Modernized visual style: replaced standard emojis with professional Material Design icons library-wide.
 
### Fixed
- **Core Stability**
  - Resolved a naming collision and Method Resolution Order (MRO) bug in the Pydantic parser hierarchy.
  - Fixed a race condition in environment variable loading within the `maticlib.llm` modules.
 
## [0.1.5] - 2026-04-12

### Added
- **OpenAI Integration**
  - Implemented `OpenAIClient` using the modern Responses API (/v1/responses).
  - Standardized response models with support for reasoning tokens (o-series) and cached tokens.
  - Full sync and async support.
- **Automated Documentation System**
  - Integrated MkDocs with the Material theme for professional, searchable documentation.
  - Automated API reference extraction from source code using `mkdocstrings`.
  - Deployment automation via GitHub Actions.
- **Example Gallery**
  - Added a comprehensive suite of examples covering basic chat, sync/async workflows, and complex graph patterns.

### Changed
- **Branding & Presentation**
  - Refined documentation aesthetics by replacing emojis with Material Design icons.
  - Standardized project leadership and contribution guidelines.

### Fixed
- **MaticGraph Engine**
  - Fixed a constructor bug where `state_schema` and `max_workers` were not properly assigned.
  - Resolved Unicode encoding issues in literal graph visualization on Windows terminals.
- **LLM Clients**
  - Improved API key validation to provide clear error messages instead of protocol errors.
  - Fixed logic bug in Gemini API key fallback mechanism.

## [0.1.4] - 2025-10-24

### Added
- **Parallel execution support in MaticGraph**
  - `parallel_group()` method for explicit fan-out/fan-in patterns
  - Execute multiple independent nodes concurrently using ThreadPoolExecutor
  - Conditional parallelization with optional condition functions
  - Join node support to aggregate parallel results
  - Configurable `max_workers` parameter for controlling concurrency
  - Automatic state merging across parallel node executions
- System instruction support for GoogleGenAIClient
  - Accept `system_instruct` parameter as string or SystemMessage object
  - Proper system instruction formatting in API requests
  - Persistent system context across conversation turns

### Changed
- **GoogleGenAIClient improvements**
  - Fixed critical payload construction bug where system instructions were lost
  - Improved API key handling with proper environment variable fallback
  - Enhanced async client resource management with context managers
  - Added timeout parameter to async requests (30 seconds)
  - Better error handling in `get_text_response()` with graceful fallbacks
- **MaticGraph visualization enhancements**
  - Graph visualization now displays parallel execution groups
  - Added visual markers (:material-shuffle-variant:) for parallel node groups
  - Shows join nodes and conditional parallelization information
  - Improved readability of complex workflow structures

### Fixed
- Fixed missing `await` on `client.aclose()` in async methods preventing resource leaks

## [0.1.3] - 2025-10-23

### Added
- **MaticGraph**: Pure-Python graph workflow engine for building agentic AI systems
  - Stateful and stateless execution modes
  - Support for dict, TypedDict, dataclass, and Pydantic BaseModel state schemas
  - Conditional branching with `add_conditional_edge()` and simplified `when()` methods
  - Node-based workflow execution with automatic state merging
  - Execution logging and text-based graph visualization
  - Loop prevention with configurable max iterations
  - Method chaining for fluent API design
- Unified response models for all LLM clients
  - `LLMResponseBase`: Common base class for standardized response handling
  - `GeminiResponse`: Pydantic model for Google Gemini API responses
  - `MistralResponse`: Pydantic model for Mistral AI API responses
  - Multimodal content support (text, image, audio, video) in response models
  - Token usage tracking with modality-specific breakdowns
- `ContentPart` class for structured multimodal content handling
- `ModalityType` enum for content type classification

### Changed
- Standardized LLM client structure across all providers
  - Consistent `_format_messages()` method implementation
  - Unified `_parse_response()` method for response handling
  - Consistent error handling and verbose logging patterns
- GoogleGenAIClient now returns `GeminiResponse` Pydantic model by default
  - Added `return_raw` parameter to optionally return raw JSON
  - Enhanced multimodal support with image, audio, and video tokens
  - Improved thinking budget and cached content token tracking
- MistralClient now returns `MistralResponse` Pydantic model by default
  - Added `return_raw` parameter for raw JSON responses
  - Enhanced Pixtral multimodal model support
  - Improved async request handling with context managers
- Enhanced `get_text_response()` helper method for both clients
  - Handles both Pydantic models and raw dict responses
  - Improved error handling for malformed responses

### Fixed
- Consistent async client cleanup in MistralClient using context managers
- Improved type hints and type safety across all LLM clients
- Enhanced error messages for invalid message formats

## [0.1.1] - 2025-10-20

### Added
- GoogleGenAIClient for Google Gemini API integration
- MistralClient for Mistral AI API integration
- LLM module with organized client structure
- Support for synchronous and asynchronous requests in all LLM clients
- Environment variable support for API keys (GOOGLE_API_KEY, MISTRAL_API_KEY)
- Flexible prompt format (string or message list) for all clients
- Multi-turn conversation support with message history
- Thinking budget configuration for Google Gemini models

### Fixed
- Fixed missing `self.` prefix in client.py payload references
- Exported BaseClientModelURL in __init__.py for easier imports

### Changed
- Updated README.md with comprehensive documentation and examples
- Reorganized package structure with dedicated llm submodule
- Enhanced error handling with detailed traceback support
- Improved license format in pyproject.toml to comply with setuptools standards

## [0.1.0] - 2025-10-19

### Added
- Initial release of maticlib
- BaseClientModelURL for custom API endpoint interactions
- Synchronous completion method
- Asynchronous completion method
- Custom ClientError exception
- Basic authentication support via headers
- Configurable verbose logging
- httpx-based HTTP client for modern async support

[Unreleased]: https://github.com/arvohsoft/maticlib/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/arvohsoft/maticlib/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/arvohsoft/maticlib/releases/tag/v0.1.0
# Changelog

All notable changes to maticlib will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
  - Added visual markers (🔀) for parallel node groups
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
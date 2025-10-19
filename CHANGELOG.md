# Changelog

All notable changes to maticlib will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
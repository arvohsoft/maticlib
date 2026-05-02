class MaticLibError(Exception):
    """Base exception class for all Maticlib errors."""
    pass

# Configuration
class ConfigurationError(MaticLibError):
    """Raised when there is a configuration issue."""
    pass

class MissingDependencyError(MaticLibError):
    """Raised by import guards when an optional dependency is missing."""
    pass

# Ingestion
class DocumentLoadError(MaticLibError):
    """Raised when a document loader fails to read a file or source."""
    pass

class ChunkingError(MaticLibError):
    """Raised when text splitting or chunking fails."""
    pass

class TabularIngestionError(MaticLibError):
    """Raised when tabular data ingestion (CSV/Excel/Parquet) fails."""
    pass

# Retrieval
class VectorIndexError(MaticLibError):
    """Raised when a vector store backend operation fails."""
    pass

class EmbeddingError(MaticLibError):
    """Raised when the embedding model provider fails."""
    pass

class RetrievalError(MaticLibError):
    """Raised when a context retrieval operation fails."""
    pass

# Generation
class LLMClientError(MaticLibError):
    """Raised when an LLM provider request fails."""
    pass

class TemplateRenderError(MaticLibError):
    """Raised when a prompt template fails to render."""
    pass

# Text2SQL
class SQLValidationError(MaticLibError):
    """Raised when generated SQL fails validation (e.g., via sqlglot)."""
    pass

class SchemaLoadError(MaticLibError):
    """Raised when a schema loader fails to parse the database schema."""
    pass

class QueryExecutionError(MaticLibError):
    """Raised when a database query execution fails."""
    pass

class DialectError(MaticLibError):
    """Raised when an unsupported or mismatched SQL dialect is encountered."""
    pass

class PromptInjectionError(MaticLibError):
    """Raised when a prompt injection attempt is detected."""
    pass

class SQLInjectionError(MaticLibError):
    """Raised when a potential SQL injection is detected in generated queries."""
    pass

# Resilience
class RetryExhaustedError(MaticLibError):
    """Raised when all retry attempts for an operation have failed."""
    pass

class FallbackExhaustedError(MaticLibError):
    """Raised when all fallbacks in a FallbackChain have failed."""
    pass

# Evaluation
class EvaluationError(MaticLibError):
    """Raised when an evaluation metric or process fails."""
    pass

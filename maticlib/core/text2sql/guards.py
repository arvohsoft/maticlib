from typing import Optional
from maticlib.exceptions import MissingDependencyError, SQLValidationError, SQLInjectionError

class SQLInjectionGuard:
    def __init__(self, allowed_dialect: str = "sqlite"):
        self.allowed_dialect = allowed_dialect
        try:
            import sqlglot
        except ImportError as e:
            raise MissingDependencyError(
                "sqlglot is required for SQLInjectionGuard. Install it with: pip install maticlib[text2sql]"
            ) from e

    def validate_and_format(self, query: str) -> str:
        """
        Validates the SQL query against injection attacks and returns a cleanly formatted
        transpiled version of the query for the target dialect.
        Ensures the query is only performing SELECT operations.
        """
        import sqlglot
        from sqlglot.errors import ParseError

        try:
            # Parse the query. sqlglot will raise if syntax is invalid
            # We parse loosely, then transpile.
            expression = sqlglot.parse_one(query, read=None)
            
            # Check if it's a select query
            if not isinstance(expression, sqlglot.exp.Select):
                raise SQLInjectionError("Only SELECT queries are allowed.")
            
            # Additional checks could be added here (e.g., preventing access to system tables)

            # Transpile and format
            safe_query = expression.sql(dialect=self.allowed_dialect, pretty=True)
            return safe_query
            
        except ParseError as e:
            raise SQLValidationError(f"Invalid SQL syntax: {e}")
        except SQLInjectionError:
            raise
        except Exception as e:
            raise SQLValidationError(f"Failed to validate SQL: {e}")

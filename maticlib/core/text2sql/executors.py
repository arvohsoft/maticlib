from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from maticlib.exceptions import MissingDependencyError, QueryExecutionError

class BaseExecutor(ABC):
    @abstractmethod
    def execute(self, query: str) -> Tuple[List[str], List[tuple]]:
        """Executes a SQL query and returns (columns, rows)."""
        pass

class SQLAlchemyExecutor(BaseExecutor):
    def __init__(self, connection_string: str, read_only: bool = True):
        self.connection_string = connection_string
        self.read_only = read_only
        try:
            from sqlalchemy import create_engine
            # If using sqlite, we can use read-only uri
            if connection_string.startswith("sqlite:///") and read_only:
                if "?" in connection_string:
                    uri = connection_string + "&mode=ro"
                else:
                    uri = connection_string + "?mode=ro"
                self.engine = create_engine(uri, creator=lambda: __import__('sqlite3').connect(uri.replace('sqlite:///', 'file:'), uri=True))
            else:
                self.engine = create_engine(connection_string)
        except ImportError as e:
            raise MissingDependencyError(
                "sqlalchemy is required for SQLAlchemyExecutor. Install it with: pip install maticlib[text2sql]"
            ) from e

    def execute(self, query: str) -> Tuple[List[str], List[tuple]]:
        try:
            from sqlalchemy import text
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = list(result.keys())
                rows = [tuple(row) for row in result.fetchall()]
                return columns, rows
        except Exception as e:
            raise QueryExecutionError(f"Failed to execute query: {e}\nQuery: {query}")

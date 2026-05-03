from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from maticlib.exceptions import MissingDependencyError, QueryExecutionError


class BaseExecutor(ABC):
    """Abstract base class for SQL query executors."""

    @abstractmethod
    def execute(self, query: str) -> Tuple[List[str], List[tuple]]:
        """
        Executes a SQL query and returns columns and rows.

        Args:
            query: A validated SELECT SQL query string.

        Returns:
            A tuple of ``(columns, rows)`` where columns is a list of column name strings
            and rows is a list of row tuples.
        """
        pass


class SQLAlchemyExecutor(BaseExecutor):
    """Executes validated SQL queries against any SQLAlchemy-supported database."""

    def __init__(self, connection_string: str, read_only: bool = True):
        """
        Initializes the SQLAlchemyExecutor.

        Args:
            connection_string: A SQLAlchemy database URI.
            read_only: If True (default), opens SQLite connections in read-only mode.
        """
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
                self.engine = create_engine(
                    uri,
                    creator=lambda: __import__("sqlite3").connect(
                        uri.replace("sqlite:///", "file:"), uri=True
                    ),
                )
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

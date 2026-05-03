from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from maticlib.core.text2sql.models import DatabaseSchema, TableSchema, ColumnSchema
from maticlib.exceptions import MissingDependencyError, SchemaLoadError


class BaseSchemaLoader(ABC):
    """Abstract base class for database schema loaders."""

    @abstractmethod
    def load_schema(self, connection_string: str) -> DatabaseSchema:
        """
        Loads and parses the schema from the given connection string.

        Args:
            connection_string: A database URI (e.g. ``sqlite:///my.db``).

        Returns:
            A fully populated DatabaseSchema object.
        """
        pass


class SQLAlchemySchemaLoader(BaseSchemaLoader):
    """Reflects a live database schema using SQLAlchemy's inspect API."""

    def load_schema(self, connection_string: str) -> DatabaseSchema:
        """
        Reflects all tables and columns from the connected database.

        Args:
            connection_string: A SQLAlchemy-compatible database URI.

        Returns:
            A DatabaseSchema containing all tables and columns.

        Raises:
            MissingDependencyError: If sqlalchemy is not installed.
            SchemaLoadError: If the schema cannot be reflected.
        """
        try:
            from sqlalchemy import create_engine, inspect
        except ImportError as e:
            raise MissingDependencyError(
                "sqlalchemy is required for SQLAlchemySchemaLoader. Install it with: pip install maticlib[text2sql]"
            ) from e

        try:
            engine = create_engine(connection_string)
            inspector = inspect(engine)

            tables = []
            for table_name in inspector.get_table_names():
                columns = []
                for col in inspector.get_columns(table_name):
                    pk = col.get("primary_key", False)
                    # Rough translation of SQLAlchemy type to string
                    data_type = str(col["type"])

                    columns.append(
                        ColumnSchema(
                            name=col["name"],
                            data_type=data_type,
                            primary_key=pk > 0 if isinstance(pk, int) else pk,
                        )
                    )

                # Fetch foreign keys
                for fk in inspector.get_foreign_keys(table_name):
                    constrained_columns = fk["constrained_columns"]
                    referred_table = fk["referred_table"]
                    referred_columns = fk["referred_columns"]

                    if constrained_columns and referred_columns:
                        col_name = constrained_columns[0]
                        ref_str = f"{referred_table}.{referred_columns[0]}"

                        # Find column and add FK
                        for c in columns:
                            if c.name == col_name:
                                c.foreign_key = ref_str
                                break

                tables.append(TableSchema(name=table_name, columns=columns))

            return DatabaseSchema(tables=tables)
        except Exception as e:
            raise SchemaLoadError(
                f"Failed to load schema from {connection_string}: {e}"
            )

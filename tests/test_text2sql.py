import pytest
import sqlite3
import os
from maticlib.core.text2sql.models import TableSchema, ColumnSchema, DatabaseSchema
from maticlib.core.text2sql.loaders import SQLAlchemySchemaLoader
from maticlib.core.text2sql.executors import SQLAlchemyExecutor
from maticlib.core.text2sql.guards import SQLInjectionGuard
from maticlib.exceptions import SQLInjectionError, SQLValidationError

def test_models_to_ddl():
    col1 = ColumnSchema(name="id", data_type="INTEGER", primary_key=True)
    col2 = ColumnSchema(name="name", data_type="VARCHAR")
    table = TableSchema(name="users", columns=[col1, col2])
    
    ddl = table.to_ddl()
    assert "CREATE TABLE users" in ddl
    assert "id INTEGER PRIMARY KEY" in ddl
    assert "name VARCHAR" in ddl

def test_schema_loader_sqlite(tmp_path):
    try:
        import sqlalchemy
    except ImportError:
        pytest.skip("sqlalchemy is required for SQLAlchemySchemaLoader tests")

    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    conn.close()

    loader = SQLAlchemySchemaLoader()
    schema = loader.load_schema(f"sqlite:///{db_path}")
    
    assert len(schema.tables) == 1
    assert schema.tables[0].name == "users"
    assert len(schema.tables[0].columns) == 2
    assert schema.tables[0].columns[0].name == "id"
    assert schema.tables[0].columns[0].primary_key is True

def test_executor_sqlite(tmp_path):
    try:
        import sqlalchemy
    except ImportError:
        pytest.skip("sqlalchemy is required for SQLAlchemyExecutor tests")

    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.commit()
    conn.close()

    executor = SQLAlchemyExecutor(f"sqlite:///{db_path}")
    columns, rows = executor.execute("SELECT * FROM users")
    
    assert columns == ["id", "name"]
    assert len(rows) == 1
    assert rows[0] == (1, "Alice")

def test_sql_injection_guard():
    try:
        import sqlglot
    except ImportError:
        pytest.skip("sqlglot is required for SQLInjectionGuard tests")

    guard = SQLInjectionGuard(allowed_dialect="sqlite")
    
    # Valid SELECT
    safe_query = guard.validate_and_format("SELECT id FROM users")
    assert "SELECT" in safe_query.upper()

    # Invalid operation (DROP)
    with pytest.raises(SQLInjectionError):
        guard.validate_and_format("DROP TABLE users")

    # Invalid operation (INSERT)
    with pytest.raises(SQLInjectionError):
        guard.validate_and_format("INSERT INTO users VALUES (1)")

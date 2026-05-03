# :material-database-search: Text2SQL (`maticlib.core.text2sql`)

Generate, validate, and safely execute SQL queries from natural language.

- **`SQLAlchemySchemaLoader`**: Auto-reflects standard databases into `TableSchema` objects.
- **`TabularIngestor`**: Easily ingests CSV, Excel, and Parquet directly into a SQL database.
- **`SQLInjectionGuard`**: Strict, syntax-level validation using `sqlglot` to prevent `DROP`, `DELETE`, and `UPDATE` tampering from rogue LLM queries.
- **`SQLAlchemyExecutor`**: Secure execution of validated queries, returning sanitized columns and rows.

```python
from maticlib.core.text2sql.guards import SQLInjectionGuard
from maticlib.core.text2sql.executors import SQLAlchemyExecutor

# Prevent destructive queries
guard = SQLInjectionGuard(allowed_dialect="postgres")
safe_query = guard.validate_and_format("SELECT * FROM users;")

# Safely execute
executor = SQLAlchemyExecutor("sqlite:///my_db.db")
cols, rows = executor.execute(safe_query)
```

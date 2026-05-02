from enum import Enum

class SQLDialect(str, Enum):
    SQLITE     = "sqlite"
    MYSQL      = "mysql"
    POSTGRESQL = "postgresql"
    BIGQUERY   = "bigquery"
    DUCKDB     = "duckdb"

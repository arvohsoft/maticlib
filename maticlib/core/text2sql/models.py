from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ColumnSchema(BaseModel):
    name: str
    data_type: str
    primary_key: bool = False
    foreign_key: Optional[str] = None
    description: Optional[str] = None

class TableSchema(BaseModel):
    name: str
    columns: List[ColumnSchema]
    description: Optional[str] = None

    def to_ddl(self, dialect: str = "sqlite") -> str:
        """
        Convert the TableSchema to a simplified DDL representation for prompts.
        We can use sqlglot or just basic formatting here.
        """
        lines = [f"CREATE TABLE {self.name} ("]
        for col in self.columns:
            pk = " PRIMARY KEY" if col.primary_key else ""
            fk = f" REFERENCES {col.foreign_key}" if col.foreign_key else ""
            lines.append(f"    {col.name} {col.data_type}{pk}{fk},")
        lines[-1] = lines[-1].rstrip(",")
        lines.append(");")
        return "\n".join(lines)

class DatabaseSchema(BaseModel):
    tables: List[TableSchema]

    def get_table_names(self) -> List[str]:
        return [t.name for t in self.tables]

    def to_prompt_string(self, subset_tables: Optional[List[str]] = None) -> str:
        """
        Returns the schema formatted for the LLM. 
        subset_tables filters which tables are included (for schema pruning).
        """
        tables_to_include = self.tables
        if subset_tables:
            tables_to_include = [t for t in self.tables if t.name in subset_tables]

        return "\n\n".join([t.to_ddl() for t in tables_to_include])

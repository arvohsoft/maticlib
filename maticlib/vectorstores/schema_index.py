from typing import List, Optional
from maticlib.core.text2sql.models import TableSchema
from maticlib.vectorstores.base_index import BaseVectorIndex
from maticlib.core.text.models import TextSegment

class SchemaVectorIndex:
    """
    A specialized wrapper around a VectorIndex for storing and retrieving 
    Database/Table schemas for Text2SQL workflows.
    """
    def __init__(self, vector_index: BaseVectorIndex):
        self.vector_index = vector_index

    def add_tables(self, tables: List[TableSchema]) -> None:
        segments = []
        for table in tables:
            ddl = table.to_ddl()
            seg = TextSegment(
                content=f"Table: {table.name}\n{ddl}",
                metadata={"table_name": table.name, "type": "schema"}
            )
            segments.append(seg)
        
        self.vector_index.add_segments(segments)

    def retrieve_relevant_tables(self, question: str, k: int = 3) -> List[str]:
        """
        Search the index for the most relevant tables given a natural language question.
        Returns a list of DDL strings.
        """
        results = self.vector_index.similarity_search(query=question, k=k, filter_dict={"type": "schema"})
        return [res.content for res in results]

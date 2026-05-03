from typing import Dict
from maticlib.prompts.base import BasePromptTemplate


class PromptRegistry:
    _templates: Dict[str, BasePromptTemplate] = {}

    @classmethod
    def register(cls, name: str, template: BasePromptTemplate):
        cls._templates[name] = template

    @classmethod
    def get(cls, name: str) -> BasePromptTemplate:
        if name not in cls._templates:
            raise KeyError(f"Template '{name}' not found in registry.")
        return cls._templates[name]


# Standard RAG Templates
RAG_QA_PROMPT = BasePromptTemplate(template="""
You are a helpful AI assistant. Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:
""")

HYDE_PROMPT = BasePromptTemplate(template="""
Please write a short passage to answer the following question. The passage should be 
detailed and contain plausible facts. Do not worry about actual factual accuracy, 
just generate what a true answer might look like.

Question: {question}

Passage:
""")

# Standard Text2SQL Templates
TEXT2SQL_GENERATION_PROMPT = BasePromptTemplate(template="""
You are an expert SQL database assistant. Given the following database schema, write a valid {dialect} SQL query that answers the user's question.
Only return the SQL query, without any markdown formatting or explanation.
Ensure the query is completely safe and uses only SELECT statements.

Schema:
{schema}

User Question: {question}

SQL Query:
""")

# Register defaults
PromptRegistry.register("rag_qa", RAG_QA_PROMPT)
PromptRegistry.register("hyde_generation", HYDE_PROMPT)
PromptRegistry.register("text2sql_generation", TEXT2SQL_GENERATION_PROMPT)

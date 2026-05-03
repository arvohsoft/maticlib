import pytest
from pydantic import BaseModel
from typing import Dict, Any
from maticlib.core.parsers.json import JSONResponseParser
from maticlib.core.parsers.pydantic import PydanticResponseParser
from maticlib.core.parsers.xml import XMLResponseParser


# --- Models for Testing ---
class User(BaseModel):
    name: str
    age: int


# --- JSON Parser Tests ---
def test_json_parser_direct():
    parser = JSONResponseParser()
    text = '{"name": "Alice", "age": 30}'
    result = parser.parse(text)
    assert result == {"name": "Alice", "age": 30}


def test_json_parser_markdown():
    parser = JSONResponseParser()
    text = (
        'Here is the data:\n```json\n{"name": "Bob", "age": 25}\n```\nHope that helps!'
    )
    result = parser.parse(text)
    assert result == {"name": "Bob", "age": 25}


def test_json_parser_braces():
    parser = JSONResponseParser()
    text = 'The result is {"name": "Charlie", "age": 40} exactly.'
    result = parser.parse(text)
    assert result == {"name": "Charlie", "age": 40}


def test_json_parser_invalid():
    parser = JSONResponseParser()
    text = "Not a JSON"
    with pytest.raises(ValueError, match="Could not parse response as JSON"):
        parser.parse(text)


# --- Pydantic Parser Tests ---
def test_pydantic_parser_success():
    parser = PydanticResponseParser(model=User)
    text = '{"name": "Alice", "age": 30}'
    result = parser.parse(text)
    assert isinstance(result, User)
    assert result.name == "Alice"
    assert result.age == 30


def test_pydantic_parser_markdown():
    parser = PydanticResponseParser(model=User)
    text = '```json\n{"name": "Bob", "age": 25}\n```'
    result = parser.parse(text)
    assert result.name == "Bob"


def test_pydantic_parser_validation_error():
    parser = PydanticResponseParser(model=User)
    text = '{"name": "Alice"}'  # Missing 'age'
    with pytest.raises(
        ValueError, match="Could not parse or validate response as Pydantic model"
    ):
        parser.parse(text)


def test_pydantic_instructions():
    parser = PydanticResponseParser(model=User)
    instructions = parser.get_structure_instructions()
    assert "properties" in instructions
    assert "name" in instructions
    assert "age" in instructions


# --- XML Parser Tests ---
def test_xml_parser_basic():
    parser = XMLResponseParser()
    text = "<user><name>Alice</name><age>30</age></user>"
    result = parser.parse(text)
    # Simple XML parser might behave differently based on implementation,
    # but based on my earlier implementation it extracts flattened tags.
    assert result["name"] == "Alice"
    assert result["age"] == "30"


def test_xml_parser_no_tags():
    parser = XMLResponseParser()
    text = "No tags here"
    with pytest.raises(ValueError, match="Could not find any XML tags"):
        parser.parse(text)

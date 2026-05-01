import pytest
from maticlib.tools import tool

def test_tool_basic_metadata():
    """Test that @tool extracts name and description correctly."""
    @tool
    def my_simple_tool():
        """This is a description."""
        return "result"
    
    assert hasattr(my_simple_tool, "matic_tool_metadata")
    metadata = my_simple_tool.matic_tool_metadata
    assert metadata["name"] == "my_simple_tool"
    assert metadata["description"] == "This is a description."
    assert metadata["parameters"]["type"] == "object"
    assert metadata["parameters"]["properties"] == {}
    assert metadata["parameters"]["required"] == []

def test_tool_parameters_schema():
    """Test that @tool generates correct JSON schema for parameters."""
    @tool
    def complex_tool(name: str, count: int, ratio: float = 1.0):
        """A tool with multiple parameter types."""
        return f"{name} {count} {ratio}"
    
    metadata = complex_tool.matic_tool_metadata
    props = metadata["parameters"]["properties"]
    
    assert props["name"]["type"] == "string"
    assert props["count"]["type"] == "integer"
    assert props["ratio"]["type"] == "number"
    
    # Required should only contain name and count (ratio has default)
    assert "name" in metadata["parameters"]["required"]
    assert "count" in metadata["parameters"]["required"]
    assert "ratio" not in metadata["parameters"]["required"]

def test_tool_list_dict_types():
    """Test that @tool handles list and dict types."""
    @tool
    def collection_tool(tags: list, metadata: dict):
        """A tool with collection types."""
        pass
    
    props = collection_tool.matic_tool_metadata["parameters"]["properties"]
    assert props["tags"]["type"] == "array"
    assert props["metadata"]["type"] == "object"

def test_tool_no_docstring():
    """Test that @tool provides a fallback description if docstring is missing."""
    @tool
    def silent_tool(x: int):
        pass
    
    assert silent_tool.matic_tool_metadata["description"] == "Function silent_tool"

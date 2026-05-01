import inspect
import functools
from typing import Any, Dict, List, get_type_hints

def _get_json_type(py_type: Any) -> str:
    """Maps Python types to JSON Schema types."""
    if py_type == str:
        return "string"
    if py_type == int:
        return "integer"
    if py_type == float:
        return "number"
    if py_type == bool:
        return "boolean"
    if py_type == list:
        return "array"
    if py_type == dict:
        return "object"
    return "string"  # Default

def tool(func):
    """
    A decorator to mark a function as a tool and automatically generate its JSON schema.
    
    This decorator inspects the function signature and docstring to create a 
    metadata dictionary used by LLM providers for function calling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Extract metadata
    name = func.__name__
    description = inspect.getdoc(func) or f"Function {name}"
    
    # Generate signature/parameters schema
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    properties = {}
    required = []
    
    for param_name, param in signature.parameters.items():
        if param_name == "self" or param_name == "cls":
            continue
            
        param_type = type_hints.get(param_name, Any)
        json_type = _get_json_type(param_type)
        
        properties[param_name] = {
            "type": json_type,
            "description": f"The {param_name} parameter." # Generic description if not available
        }
        
        if param.default is inspect.Parameter.empty:
            required.append(param_name)

    # Attach tool metadata to the wrapper function
    wrapper.matic_tool_metadata = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }
    
    return wrapper
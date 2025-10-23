from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

@dataclass
class Node:
    """Represents a node in the graph"""
    name: str
    function: Callable
    next_nodes: List[str] = field(default_factory=list)
    condition_func: Optional[Callable] = None
    condition_map: Optional[Dict[str, str]] = None
    readable_names: Optional[Dict[str, str]] = None
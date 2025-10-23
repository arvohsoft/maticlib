from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional, List

@dataclass
class Node:
    """Represents a node in the graph"""
    name: str
    function: Callable
    next_nodes: List[str] = field(default_factory=list)
    condition_func: Optional[Callable] = None
    condition_map: Optional[Dict[str, str]] = None
    readable_names: Optional[Dict[str, str]] = None
    
    # Parallel execution support
    parallel_group: Optional[List[str]] = None
    parallel_join: Optional[str] = None
    parallel_condition: Optional[Callable] = None
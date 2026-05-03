from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional, List


@dataclass
class Node:
    """
    Represents a processing node within a MaticGraph workflow.

    A node encapsulates a function to be executed and metadata for
    routing the workflow after execution, including support for
    conditional branching and parallel execution.

    Attributes:
        name (str): Unique identifier for the node.
        function (Callable): The Python function to execute. Receives the current
            state and returns an update (dict or model).
        next_nodes (List[str]): List of possible next nodes for sequential or parallel flow.
        condition_func (Optional[Callable]): A function that determines which
            route to take next based on the returned key.
        condition_map (Optional[Dict[str, str]]): Maps keys from `condition_func`
            to target node names.
        readable_names (Optional[Dict[str, str]]): Human-readable names for routes
            (useful for visualization).
        parallel_group (Optional[List[str]]): List of nodes to execute in
            parallel after this node.
        parallel_join (Optional[str]): A node where parallel execution groups
            re-converge.
        parallel_condition (Optional[Callable]): A condition to decide whether
            to trigger parallel execution.
    """

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

from typing import Callable, Dict, Any, Optional, List, Union, Set
from .node import Node
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from pydantic import BaseModel
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseModel = None


class MaticGraph:
    """
    A fast, pure-Python graph workflow engine with optional state management.
    Supports dict, TypedDict, dataclass, and Pydantic BaseModel states.
    
    Args:
        stateful: If True, maintains and merges state across nodes.
        state_schema: Optional Pydantic BaseModel, dataclass, or TypedDict class
        max_workers: Maximum number of parallel workers (default: 4)
    """
    
    def __init__(
        self,
        stateful: bool = True,
        state_schema: Optional[type] = None,
        max_workers: int = 4
    ):
        self.stateful = stateful
        self.state_schema = state_schema
        self.max_workers = max_workers
        self.nodes: Dict[str, Node] = {}
        self.entry_node: Optional[str] = None
        self.exit_nodes: List[str] = []
        self._execution_log: List[Dict[str, Any]] = []
        self._parallel_groups: Dict[str, List[str]] = {}  # Maps trigger node to parallel nodes
        
        # Detect if state_schema is a Pydantic model
        self._is_pydantic = False
        if state_schema is not None and PYDANTIC_AVAILABLE:
            self._is_pydantic = (
                isinstance(state_schema, type) and 
                issubclass(state_schema, BaseModel)
            )
    
    def add_node(self, name: str, function: Callable) -> 'MaticGraph':
        """Add a processing node to the graph."""
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")
        
        self.nodes[name] = Node(name=name, function=function)
        return self
    
    def add_edge(self, from_node: str, to_node: str) -> 'MaticGraph':
        """Add a direct connection between two nodes."""
        if from_node not in self.nodes:
            raise ValueError(f"Source node '{from_node}' not found")
        if to_node not in self.nodes and to_node != "END":
            raise ValueError(f"Destination node '{to_node}' not found")
        
        self.nodes[from_node].next_nodes.append(to_node)
        return self
    
    def parallel_group(
        self,
        from_node: str,
        parallel_nodes: List[str],
        join_node: Optional[str] = None,
        condition: Optional[Callable[[Any], bool]] = None
    ) -> 'MaticGraph':
        """
        Execute multiple nodes in parallel after a specific node.
        
        Args:
            from_node: Node that triggers parallel execution
            parallel_nodes: List of nodes to execute in parallel
            join_node: Optional node to execute after all parallel nodes complete
            condition: Optional function to decide whether to parallelize
                      If returns False, executes first parallel_node only
        
        Example:
            # Always parallel
            graph.parallel_group(
                "analyze",
                ["sentiment", "entities", "summary"],
                join_node="combine_results"
            )
            
            # Conditional parallel
            graph.parallel_group(
                "check_size",
                ["process_large_a", "process_large_b"],
                join_node="merge",
                condition=lambda state: state.get("size") > 1000
            )
        """
        # Validate nodes exist
        if from_node not in self.nodes:
            raise ValueError(f"Trigger node '{from_node}' not found")
        
        for node in parallel_nodes:
            if node not in self.nodes:
                raise ValueError(f"Parallel node '{node}' not found")
        
        if join_node and join_node not in self.nodes:
            raise ValueError(f"Join node '{join_node}' not found")
        
        # Store parallel group configuration
        self._parallel_groups[from_node] = {
            "nodes": parallel_nodes,
            "join_node": join_node,
            "condition": condition
        }
        
        # Mark the trigger node as having parallel execution
        self.nodes[from_node].parallel_group = parallel_nodes
        self.nodes[from_node].parallel_join = join_node
        self.nodes[from_node].parallel_condition = condition
        
        return self
    
    def add_conditional_edge(
        self,
        from_node: str,
        condition: Callable[[Any], str],
        routes: Dict[str, str],
        readable_names: Optional[Dict[str, str]] = None
    ) -> 'MaticGraph':
        """Add a conditional edge that routes based on condition output."""
        if from_node not in self.nodes:
            raise ValueError(f"Node '{from_node}' not found")
        
        for route_key, target in routes.items():
            if target not in self.nodes and target != "END":
                raise ValueError(f"Route target '{target}' not found")
        
        node = self.nodes[from_node]
        node.condition_func = condition
        node.condition_map = routes
        node.readable_names = readable_names or {}
        
        return self
    
    def when(self, from_node: str, **routes: str) -> 'MaticGraph':
        """
        Simplified conditional routing using state['next'] or state.next
        Works with both dict and Pydantic models.
        """
        def route_by_next(state: Any) -> str:
            # Handle Pydantic models
            if self._is_pydantic and isinstance(state, BaseModel):
                next_key = getattr(state, 'next', None)
            # Handle dicts and TypedDict
            elif isinstance(state, dict):
                next_key = state.get("next")
            else:
                # Handle dataclasses
                next_key = getattr(state, 'next', None)
            
            if next_key not in routes:
                available = ", ".join(routes.keys())
                raise ValueError(
                    f"Invalid route '{next_key}'. Available routes: {available}"
                )
            return next_key
        
        return self.add_conditional_edge(
            from_node,
            route_by_next,
            routes,
            readable_names={k: k.replace("_", " ").title() for k in routes.keys()}
        )
    
    def set_entry(self, node_name: str) -> 'MaticGraph':
        """Set the starting node."""
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found")
        self.entry_node = node_name
        return self
    
    def set_exit(self, node_name: str) -> 'MaticGraph':
        """Mark a node as an exit point."""
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found")
        if node_name not in self.exit_nodes:
            self.exit_nodes.append(node_name)
        return self
    
    def _merge_state(self, current: Any, update: Any) -> Any:
        """
        Merge state updates intelligently.
        Supports dict, Pydantic models, and dataclasses.
        """
        if not self.stateful:
            return update if update else current
        
        # Handle Pydantic models
        if self._is_pydantic:
            if isinstance(current, BaseModel):
                if isinstance(update, dict):
                    update_data = current.model_dump()
                    update_data.update(update)
                    return self.state_schema(**update_data)
                elif isinstance(update, BaseModel):
                    update_data = current.model_dump()
                    update_data.update(update.model_dump(exclude_unset=True))
                    return self.state_schema(**update_data)
            else:
                if isinstance(update, dict):
                    return self.state_schema(**update)
                return update
        
        # Handle dict-based state
        if isinstance(current, dict):
            for key, value in (update.items() if isinstance(update, dict) else vars(update).items()):
                if key in current:
                    if isinstance(current[key], list) and isinstance(value, list):
                        current[key].extend(value)
                    elif isinstance(current[key], dict) and isinstance(value, dict):
                        current[key].update(value)
                    else:
                        current[key] = value
                else:
                    current[key] = value
            return current
        
        # Handle dataclasses
        if hasattr(current, '__dataclass_fields__'):
            update_dict = vars(current).copy()
            if isinstance(update, dict):
                update_dict.update(update)
            else:
                update_dict.update(vars(update))
            return type(current)(**update_dict)
        
        return update if update else current
    
    def _execute_node(self, node_name: str, state: Any) -> Any:
        """Execute a single node and return updated state."""
        node = self.nodes[node_name]
        start_time = time.time()
        
        try:
            result = node.function(state)
            
            if result is None:
                result = {}
            
            # Don't merge state here if we're in a parallel group
            # The parallel executor will handle merging
            updated_state = result if not self.stateful else self._merge_state(state, result)
            
            execution_time = time.time() - start_time
            
            # Log execution
            if self._is_pydantic and isinstance(updated_state, BaseModel):
                state_keys = list(updated_state.model_fields.keys())
            elif isinstance(updated_state, dict):
                state_keys = list(updated_state.keys())
            else:
                state_keys = list(vars(updated_state).keys()) if hasattr(updated_state, '__dict__') else []
            
            self._execution_log.append({
                "node": node_name,
                "status": "success",
                "execution_time": execution_time,
                "state_keys": state_keys
            })
            
            return updated_state
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._execution_log.append({
                "node": node_name,
                "status": "error",
                "execution_time": execution_time,
                "error": str(e)
            })
            raise RuntimeError(f"Error in node '{node_name}': {str(e)}") from e
    
    def _execute_parallel_group(
        self,
        parallel_nodes: List[str],
        state: Any,
        verbose: bool = False
    ) -> Any:
        """
        Execute a group of nodes in parallel and merge their results.
        """
        if verbose:
            print(f"\n  🔀 Executing {len(parallel_nodes)} nodes in parallel: {parallel_nodes}")
        
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(parallel_nodes))) as executor:
            # Submit all parallel nodes
            future_to_node = {
                executor.submit(self._execute_node, node_name, state): node_name
                for node_name in parallel_nodes
            }
            
            # Collect results
            results = {}
            for future in as_completed(future_to_node):
                node_name = future_to_node[future]
                try:
                    node_result = future.result()
                    results[node_name] = node_result
                    if verbose:
                        print(f"    ✓ {node_name} completed")
                except Exception as e:
                    raise RuntimeError(f"Parallel node '{node_name}' failed: {e}") from e
            
            # Merge all results into state
            merged_state = state
            for node_name in parallel_nodes:
                if self.stateful:
                    merged_state = self._merge_state(merged_state, results[node_name])
                else:
                    merged_state = results[node_name]  # Last result wins in stateless
            
            return merged_state
    
    def _get_next_node(self, current_node: str, state: Any) -> Optional[Union[str, List[str]]]:
        """
        Determine the next node(s) based on edges and conditions.
        Returns either a single node name or a list for parallel execution.
        """
        node = self.nodes[current_node]
        
        if current_node in self.exit_nodes:
            return None
        
        # Check for parallel group execution
        if hasattr(node, 'parallel_group') and node.parallel_group:
            # Check condition if exists
            if hasattr(node, 'parallel_condition') and node.parallel_condition:
                should_parallelize = node.parallel_condition(state)
                if not should_parallelize:
                    # Execute first node only (sequential fallback)
                    return node.parallel_group[0]
            
            # Return special marker for parallel execution
            return ("PARALLEL", node.parallel_group, node.parallel_join)
        
        # Check conditional routing
        if node.condition_func:
            try:
                route_key = node.condition_func(state)
                next_node = node.condition_map.get(route_key)
                
                if next_node is None:
                    raise ValueError(
                        f"Condition returned invalid key '{route_key}'. "
                        f"Valid keys: {list(node.condition_map.keys())}"
                    )
                
                readable = node.readable_names.get(route_key, route_key)
                self._execution_log.append({
                    "type": "routing",
                    "from": current_node,
                    "to": next_node,
                    "route": readable
                })
                
                return None if next_node == "END" else next_node
                
            except Exception as e:
                raise RuntimeError(
                    f"Condition function failed in node '{current_node}': {str(e)}"
                ) from e
        
        # Regular edge
        if node.next_nodes:
            next_node = node.next_nodes[0]
            return None if next_node == "END" else next_node
        
        return None
    
    def run(
        self,
        initial_state: Optional[Union[Dict[str, Any], BaseModel]] = None,
        max_iterations: int = 1000,
        verbose: bool = False
    ) -> Union[Dict[str, Any], BaseModel]:
        """
        Execute the graph workflow with support for parallel node groups.
        
        Args:
            initial_state: Starting state (dict, Pydantic model, or dataclass)
            max_iterations: Maximum nodes to execute
            verbose: Print execution details
        
        Returns:
            Final state after execution
        """
        if self.entry_node is None:
            raise RuntimeError("No entry node set. Call set_entry() first.")
        
        self._execution_log = []
        
        # Initialize state based on schema
        if initial_state is None:
            if self._is_pydantic:
                state = self.state_schema()
            elif self.state_schema:
                state = self.state_schema()
            else:
                state = {}
        else:
            if self._is_pydantic and isinstance(initial_state, dict):
                state = self.state_schema(**initial_state)
            else:
                state = initial_state
        
        current_node = self.entry_node
        iteration = 0
        
        if verbose:
            print(f"Starting execution at node: {current_node}")
            print(f"Initial state: {state}\n")
        
        while current_node is not None and iteration < max_iterations:
            iteration += 1
            
            if verbose:
                print(f"[{iteration}] Executing node: {current_node}")
            
            # Execute current node
            state = self._execute_node(current_node, state)
            
            if verbose:
                print(f"    State after: {state}")
            
            # Get next node(s)
            next_node = self._get_next_node(current_node, state)
            
            # Check if next is a parallel group
            if isinstance(next_node, tuple) and next_node[0] == "PARALLEL":
                _, parallel_nodes, join_node = next_node
                
                # Execute parallel nodes
                state = self._execute_parallel_group(parallel_nodes, state, verbose)
                
                # Continue to join node if specified
                if join_node:
                    current_node = join_node
                    if verbose:
                        print(f"  ⚡ Parallel execution complete, continuing to: {join_node}\n")
                else:
                    # No join node, end execution
                    current_node = None
            else:
                # Regular sequential execution
                if verbose and next_node:
                    print(f"    Next: {next_node}\n")
                elif verbose:
                    print(f"    Workflow complete\n")
                
                current_node = next_node
        
        if iteration >= max_iterations:
            raise RuntimeError(
                f"Maximum iterations ({max_iterations}) reached. "
                "Possible infinite loop in graph."
            )
        
        return state
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get detailed execution log from last run."""
        return self._execution_log
    
    def visualize(self) -> str:
        """Generate a text-based visualization of the graph."""
        lines = ["Graph Structure:", "=" * 50]
        
        if self.state_schema:
            schema_name = getattr(self.state_schema, '__name__', str(self.state_schema))
            state_type = "Pydantic Model" if self._is_pydantic else "Schema"
            lines.append(f"State {state_type}: {schema_name}")
        
        lines.append(f"Max Workers: {self.max_workers}")
        lines.append("")
        
        for node_name, node in self.nodes.items():
            marker = "►" if node_name == self.entry_node else "•"
            exit_marker = " [EXIT]" if node_name in self.exit_nodes else ""
            
            # Check if node has parallel group
            parallel_marker = ""
            if hasattr(node, 'parallel_group') and node.parallel_group:
                parallel_marker = f" 🔀 [PARALLEL→{len(node.parallel_group)} nodes]"
            
            lines.append(f"{marker} {node_name}{exit_marker}{parallel_marker}")
            
            # Show parallel group details
            if hasattr(node, 'parallel_group') and node.parallel_group:
                lines.append(f"  ├─ Parallel nodes:")
                for pnode in node.parallel_group:
                    lines.append(f"  │  └─ {pnode}")
                if hasattr(node, 'parallel_join') and node.parallel_join:
                    lines.append(f"  └─ Join at: {node.parallel_join}")
            
            # Show conditional routing
            if node.condition_func:
                lines.append(f"  └─ Conditional routing:")
                for route_key, target in node.condition_map.items():
                    readable = node.readable_names.get(route_key, route_key)
                    lines.append(f"     [{route_key}] → {target} ({readable})")
            # Show regular edges
            elif not hasattr(node, 'parallel_group'):
                for next_node in node.next_nodes:
                    lines.append(f"  └─→ {next_node}")
        
        return "\n".join(lines)
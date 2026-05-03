# :material-sitemap-outline: MaticGraph (`maticlib.graph`)

A high-performance orchestration engine for building complex AI workflows as directed graphs.

### **The Architecture**

```python
from maticlib.graph import MaticGraph

# Initialize with an optional state schema (Pydantic model recommended)
graph = MaticGraph(stateful=True, state_schema=MyStateModel)

# 1. Add Nodes (Pure Python functions)
def my_node(state: MyStateModel):
    return {"data": "processed"}

graph.add_node("PROCESS", my_node)

# 2. Define Edges (Routing)
graph.add_edge("START", "PROCESS")
graph.set_entry("START")

# 3. Execution
final_state = graph.run(initial_state={"input": "data"}, verbose=True)
```

### **Advanced Routing**

- **`parallel_group(from_node, parallel_nodes, join_node)`**: Execute multiple nodes concurrently.
- **`add_conditional_edge(from_node, condition_func, routes)`**: Route dynamically based on code logic.
- **`when(from_node, **routes)`**: Simple routing based on a `next` field in the state.

```python
# Example: Using .when for simple intent routing
graph.when("classifier", 
    chat="chat_node",
    search="web_search_node",
    complete="END"
)
```

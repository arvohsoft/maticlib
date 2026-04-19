"""
Example: Sequential Workflow with MaticGraph
============================================
This example demonstrates a simple linear workflow where data flows through 
multiple processing nodes.
"""

from maticlib.graph import MaticGraph

def extract_name(state):
    """Simple node to 'extract' a name from input"""
    input_text = state.get("input", "")
    # Simulation: find a name in string
    name = input_text.split()[-1] if input_text else "World"
    print(f"[Node 1] Extracted name: {name}")
    return {"name": name}

def generate_greeting(state):
    """Node to create a greeting using the extracted name"""
    name = state.get("name")
    greeting = f"Hello, {name}!"
    print(f"[Node 2] Generated greeting: {greeting}")
    return {"greeting": greeting}

def run_sequential_graph():
    # 1. Initialize the graph
    graph = MaticGraph(stateful=True)
    
    # 2. Add nodes
    graph.add_node("extract", extract_name)
    graph.add_node("greet", generate_greeting)
    
    # 3. Define edges (connections)
    graph.add_edge("extract", "greet")
    graph.add_edge("greet", "END")
    
    # 4. Set the starting point
    graph.set_entry("extract")
    
    print("Running sequential graph...\n")
    
    # 5. Execute the graph with initial data
    final_state = graph.run({"input": "My name is Alice"}, verbose=True)
    
    print(f"\nFinal state: {final_state}")
    print("\nGraph Visualization:")
    print(graph.visualize())

if __name__ == "__main__":
    run_sequential_graph()

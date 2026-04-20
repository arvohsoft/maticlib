"""
Example: Typed State with Pydantic
==================================
This example demonstrates how to use a Pydantic BaseModel as the state 
for a MaticGraph, providing validation and auto-completion.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from maticlib.graph import MaticGraph

# 1. Define your state schema
class ResearchState(BaseModel):
    topic: str
    summary: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    next: str = "analyze"  # Default routing key

# 2. Define nodes that work with the model
def start_research(state: ResearchState):
    print(f"Researching topic: {state.topic}")
    return {
        "sources": ["Wikipedia", "ArXiv", "News"],
        "next": "evaluate"
    }

def evaluate_sources(state: ResearchState):
    print(f"Evaluating {len(state.sources)} sources...")
    return {
        "summary": f"Findings on {state.topic}...",
        "next": "END"
    }

def run_typed_graph():
    # 3. Create graph with the schema
    graph = MaticGraph(state_schema=ResearchState)
    
    graph.add_node("search", start_research)
    graph.add_node("analyze", evaluate_sources)
    
    # 4. Use the .when() helper for easy Pydantic-based routing
    # It automatically checks state.next
    graph.when("search", evaluate="analyze")
    graph.add_edge("analyze", "END")
    
    graph.set_entry("search")
    
    print("Running graph with Pydantic state...\n")
    
    # Run with initial dict (automatically cast to ResearchState) 
    # or pass a ResearchState instance.
    initial_data = {"topic": "Artificial Intelligence"}
    final_state = graph.run(initial_data, verbose=True)
    
    print(f"\nFinal state Type: {type(final_state)}")
    print(f"Summary: {final_state.summary}")

if __name__ == "__main__":
    run_typed_graph()

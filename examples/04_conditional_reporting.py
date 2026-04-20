"""
Example: Conditional Routing with MaticGraph
============================================
This example shows how to use add_conditional_edge to route execution 
based on the output of a node (e.g., sentiment analysis).
"""

from maticlib.graph import MaticGraph

def analyze_sentiment(state):
    """Simulates sentiment analysis"""
    text = state.get("text", "").lower()
    if "good" in text or "happy" in text:
        sentiment = "positive"
    elif "bad" in text or "sad" in text:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    print(f"[Analyze] Sentiment detected: {sentiment}")
    return {"sentiment": sentiment}

def handle_positive(state):
    print("[Handler] Writing a cheerful response...")
    return {"response": "We are glad you are happy!"}

def handle_negative(state):
    print("[Handler] Writing an apologetic response...")
    return {"response": "We are sorry you had a bad experience."}

def handle_neutral(state):
    print("[Handler] Writing a standard response...")
    return {"response": "Thank you for your feedback."}

def run_conditional_graph():
    graph = MaticGraph()
    
    # Add nodes
    graph.add_node("analyze", analyze_sentiment)
    graph.add_node("positive_flow", handle_positive)
    graph.add_node("negative_flow", handle_negative)
    graph.add_node("neutral_flow", handle_neutral)
    
    # Define conditional routing
    # This function looks at the state and returns a key used in the mapping below
    def check_sentiment(state):
        return state.get("sentiment")
    
    graph.add_conditional_edge(
        "analyze",
        condition=check_sentiment,
        routes={
            "positive": "positive_flow",
            "negative": "negative_flow",
            "neutral": "neutral_flow"
        }
    )
    
    # Close the loops
    graph.add_edge("positive_flow", "END")
    graph.add_edge("negative_flow", "END")
    graph.add_edge("neutral_flow", "END")
    
    graph.set_entry("analyze")
    
    print("Test Case 1: Positive Sentiment")
    graph.run({"text": "I had a very good day!"})
    
    print("\nTest Case 2: Negative Sentiment")
    graph.run({"text": "The service was bad."})

if __name__ == "__main__":
    run_conditional_graph()

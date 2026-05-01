import os
from typing import Annotated
from dotenv import load_dotenv
from maticlib.llm.openai import OpenAIClient
from maticlib.tools import tool

# Load API keys from .env
load_dotenv()

# 1. Define a tool with @tool
@tool
def get_weather(location: str):
    """
    Get the current weather in a given location.
    """
    # In a real app, this would call a weather API
    return f"The weather in {location} is sunny and 25°C."

@tool
def calculate_area(radius: int):
    """
    Calculate the area of a circle.
    """
    import math
    return math.pi * (radius ** 2)

# 2. Initialize the client
client = OpenAIClient(model="gpt-4o-mini")

# 3. Request completion with tools
# We ask a question that requires a tool call
prompt = "What is the weather in Paris and what is the area of a circle with radius 5?"

print(f"Prompt: {prompt}")
print("-" * 30)

response = client.complete(
    input=prompt,
    tools=[get_weather, calculate_area]
)

# 4. Check for tool calls
if response.tool_calls:
    print(f"Model requested {len(response.tool_calls)} tool calls:")
    for call in response.tool_calls:
        name = call["function"]["name"]
        args = call["function"]["arguments"]
        print(f" - Tool: {name}")
        print(f" - Args: {args}")
        
        # In a real agent loop, we would execute these and send results back
else:
    print("No tool calls requested.")
    print(f"Response: {response.content}")

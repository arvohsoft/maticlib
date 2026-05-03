"""
Example: OpenAI Simple Chat
===========================
A focused example showing how to use the OpenAIClient with the Responses API.

This script demonstrates:
1. Loading API keys from .env
2. Synchronous text completion
3. Accessing metadata like token usage and reasoning tokens
"""

import os
from dotenv import load_dotenv
from maticlib.llm.openai import OpenAIClient
from maticlib.messages import HumanMessage, SystemMessage

# 1. Load your API key from the .env file in the project root
# (Automatically searches project root and current directory)
load_dotenv()
# load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def run_openai_example():
    # 2. Initialize the client
    # It will automatically use OPENAI_API_KEY from your environment.
    try:
        client = OpenAIClient(
            model="gpt-4o-mini",  # You can use any model: gpt-4o, o1-mini, gpt-5.4, etc.
            verbose=True,
        )
    except ValueError as e:
        print(f"❌ Error: {e}")
        return

    # 3. Simple text completion
    prompt = "What are the benefits of using a graph-based workflow for AI agents?"

    print(f"\n--- Sending Prompt ---\n{prompt}")

    try:
        response = client.complete(prompt)

        # 4. Extract text response
        text = client.get_text_response(response)
        print(f"\n--- Response ---\n{text}")

        # 5. Access rich metadata provided by the Responses API
        print(f"\n--- Metadata ---")
        print(f"Response ID: {response.response_id}")
        print(f"Model used:  {response.model_version}")
        print(f"Usage:")
        print(f"  - Prompt tokens:     {response.prompt_tokens}")
        print(f"  - Completion tokens: {response.completion_tokens}")
        print(f"  - Total tokens:      {response.total_tokens}")

        # These are specific to OpenAI's newer models
        if response.cached_tokens:
            print(f"  - Cached tokens:     {response.cached_tokens} (saved money!)")
        if response.reasoning_tokens:
            print(
                f"  - Reasoning tokens:  {response.reasoning_tokens} (o-series thinking)"
            )

    except Exception as e:
        print(f"❌ API Call Failed: {e}")


if __name__ == "__main__":
    run_openai_example()

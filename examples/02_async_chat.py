"""
Example: Async Concurrent Chat
==============================
This example shows how to use the async_complete method to send requests 
to multiple providers concurrently, reducing total wait time.
"""

import asyncio
import os
from dotenv import load_dotenv
from maticlib.llm.openai import OpenAIClient
from maticlib.llm.mistral import MistralClient
from maticlib.llm.google_genai import GoogleGenAIClient

# Load environment variables from current directory or parent (project root)
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def check_keys():
    """Checks if required API keys are available and prints helpful hints."""
    keys = {
        "OPENAI_API_KEY": "OpenAI",
        "MISTRAL_API_KEY": "Mistral",
        "GOOGLE_API_KEY": "Google Gemini"
    }
    missing = [name for name, provider in keys.items() if not os.getenv(name)]
    
    if missing:
        print("⚠️  Warning: Missing API keys in environment!")
        print("Please ensure your .env file exists in the project root and contains:")
        for key in missing:
            print(f"  - {key}")
        print("\nYou can copy .env.example to .env to get started.\n")
    return missing

async def run_async_chat():
    missing = check_keys()
    
    # Initialize clients only if their keys are present to avoid protocol errors
    clients_to_run = []
    providers = []
    
    if "OPENAI_API_KEY" not in missing:
        clients_to_run.append(OpenAIClient())
        providers.append("OpenAI")
    
    if "MISTRAL_API_KEY" not in missing:
        clients_to_run.append(MistralClient())
        providers.append("Mistral")
        
    if "GOOGLE_API_KEY" not in missing:
        clients_to_run.append(GoogleGenAIClient())
        providers.append("Gemini")

    if not clients_to_run:
        print("No API keys found. Skipping chat requests.")
        return
    
    prompt = "What are the three laws of robotics?"
    
    print(f"Sending requests concurrently for: '{prompt}'\n")
    
    # Create tasks for parallel execution
    tasks = [client.async_complete(prompt) for client in clients_to_run]
    
    # Run all tasks and wait for results
    print("Waiting for responses...")
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for provider, client, result in zip(providers, clients_to_run, results):
        print(f"\n--- {provider} ---")
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(client.get_text_response(result))

if __name__ == "__main__":
    asyncio.run(run_async_chat())

"""
Example: Basic Sync Chat
========================
This example shows how to initialize and use LLM clients from different
providers (OpenAI, Mistral, Google Gemini) to send simple chat requests.

Prerequisites:
Set up your .env file with the following keys:
- OPENAI_API_KEY
- MISTRAL_API_KEY
- GOOGLE_API_KEY
"""

import os
from dotenv import load_dotenv
from maticlib.llm.openai import OpenAIClient
from maticlib.llm.mistral import MistralClient
from maticlib.llm.google_genai import GoogleGenAIClient
from maticlib.messages import HumanMessage

# Load environment variables from current directory or parent (project root)
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def check_keys():
    """Checks if required API keys are available and prints helpful hints."""
    keys = {
        "OPENAI_API_KEY": "OpenAI",
        "MISTRAL_API_KEY": "Mistral",
        "GOOGLE_API_KEY": "Google Gemini",
    }
    missing = [
        name for name, provider in keys.items() if not (os.getenv(name) or "").strip()
    ]

    if missing:
        print("⚠️  Warning: Missing API keys in environment!")
        print("Please ensure your .env file exists in the project root and contains:")
        for key in missing:
            print(f"  - {key}")
        print("\nYou can copy .env.example to .env to get started.\n")
    return missing


def run_basic_chat():
    missing = check_keys()

    # Initialize clients only if their keys are present to avoid protocol errors
    openai = OpenAIClient(verbose=True) if "OPENAI_API_KEY" not in missing else None
    mistral = (
        MistralClient(model="mistral-large-latest")
        if "MISTRAL_API_KEY" not in missing
        else None
    )
    gemini = (
        GoogleGenAIClient(model="gemini-2.5-flash-lite")
        if "GOOGLE_API_KEY" not in missing
        else None
    )

    prompt = "Explain quantum computing in one sentence."

    print(f"\nPrompt: {prompt}\n")
    print("-" * 50)

    # --- OpenAI ---
    print("\n[OpenAI Response]")
    if openai:
        try:
            response = openai.complete(prompt)
            print(openai.get_text_response(response))
        except Exception as e:
            print(f"OpenAI Error: {e}")
    else:
        print("Skipping OpenAI: API key not found.")

    # --- Mistral ---
    print("\n[Mistral Response]")
    if mistral:
        try:
            response = mistral.complete(prompt)
            print(mistral.get_text_response(response))
        except Exception as e:
            print(f"Mistral Error: {e}")
    else:
        print("Skipping Mistral: API key not found.")

    # --- Gemini ---
    print("\n[Gemini Response]")
    if gemini:
        try:
            response = gemini.complete(prompt)
            print(gemini.get_text_response(response))
        except Exception as e:
            print(f"Gemini Error: {e}")
    else:
        print("Skipping Gemini: API key not found.")


if __name__ == "__main__":
    run_basic_chat()

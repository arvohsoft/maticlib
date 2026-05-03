import os
from pydantic import BaseModel, Field
from maticlib.llm.openai import OpenAIClient
from maticlib.llm.google_genai import GoogleGenAIClient
from maticlib.llm.mistral import MistralClient
from dotenv import load_dotenv

# Load API keys from .env if present
load_dotenv()


# 1. Define your desired response structure
class CountryInfo(BaseModel):
    name: str = Field(..., description="Full name of the country")
    capital: str = Field(..., description="Capital city")
    population: int = Field(..., description="Approximate population")
    is_landlocked: bool = Field(..., description="Whether the country is landlocked")


def verify_provider(name, client, query):
    print(f"\n--- Verifying {name} ---")
    try:
        response = client.complete(query, response_model=CountryInfo)

        # Access the parsed object
        country_data = response.parsed_output

        if country_data:
            print(f"[SUCCESS] Successfully Parsed into {type(country_data).__name__}")
            print(f"Data: {country_data.model_dump()}")
        else:
            print(f"[ERROR] Failed to parse output for {name}.")
            print(f"Raw Content: {response.content}")
    except Exception as e:
        print(f"[WARNING] Error verifying {name}: {e}")


def main():
    query = "Give me information about India in a single JSON object."

    # 1. OpenAI
    if os.getenv("OPENAI_API_KEY"):
        verify_provider(
            "OpenAI (gpt-4o-mini)",
            OpenAIClient(model="gpt-4o-mini", verbose=False),
            query,
        )
    else:
        print("\nSkipping OpenAI: OPENAI_API_KEY not set.")

    # 2. Google Gemini
    if os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"):
        verify_provider(
            "Google Gemini (gemini-2.5-flash-lite)",
            GoogleGenAIClient(model="gemini-2.5-flash-lite", verbose=False),
            query,
        )
    else:
        print("\nSkipping Gemini: GOOGLE_API_KEY not set.")

    # 3. Mistral AI
    if os.getenv("MISTRAL_API_KEY"):
        verify_provider(
            "Mistral AI (mistral-small-latest)",
            MistralClient(model="mistral-small-latest", verbose=False),
            query,
        )
    else:
        print("\nSkipping Mistral: MISTRAL_API_KEY not set.")


if __name__ == "__main__":
    main()

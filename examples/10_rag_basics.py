"""
RAG Basics - Embeddings
========================
This example demonstrates how to use Maticlib's unified Embeddings interface
to generate vector representations of text using different providers.
"""

from maticlib.embeddings import (
    OpenAIEmbeddings,
    GoogleGenAIEmbeddings,
    MistralEmbeddings,
)
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    # 1. Initialize OpenAI Embeddings
    try:
        openai_embed = OpenAIEmbeddings(model="text-embedding-3-small", verbose=True)

        # Embed a single query
        query = "What are the core features of Maticlib?"
        res = openai_embed.embed_query(query)
        print(f"\n[OpenAI] Response Model: {res.model}")
        print(f"[OpenAI] Query Vector (first 5 dims): {res.vector[:5]}...")
        print(f"[OpenAI] Total Dimensions: {len(res.vector)}")
        print(f"[OpenAI] Tokens Used: {res.prompt_tokens}")

    except Exception as e:
        print(f"Skipping OpenAI example: {e}")

    # 2. Initialize Google Gemini Embeddings
    try:
        google_embed = GoogleGenAIEmbeddings(model="gemini-embedding-001", verbose=True)

        # Embed multiple documents in a batch
        docs = [
            "Maticlib is a high-performance Python library for creating AI agents.",
            "It supports multiple providers including OpenAI, Gemini, and Mistral.",
            "The library focuses on type safety and graph-based orchestration.",
        ]
        res = google_embed.embed_documents(docs)

        print(f"\n[Google] Response Model: {res.model}")
        print(f"[Google] Embedded {len(res.vectors)} documents.")
        print(f"[Google] First Doc Vector (first 5 dims): {res.vectors[0][:5]}...")
        print(f"[Google] Total Dimensions: {len(res.vectors[0])}")
        print(f"[Google] Tokens Used: {res.prompt_tokens}")

    except Exception as e:
        print(f"Skipping Google example: {e}")

    # 3. Initialize Mistral Embeddings
    try:
        mistral_embed = MistralEmbeddings(model="mistral-embed", verbose=True)

        # Embed a single query
        query = "How to integrate API keys?"
        res = mistral_embed.embed_query(query)

        print(f"\n[Mistral] Response Model: {res.model}")
        print(f"[Mistral] Query Vector (first 5 dims): {res.vector[:5]}...")
        print(f"[Mistral] Total Dimensions: {len(res.vector)}")
        print(f"[Mistral] Tokens Used: {res.prompt_tokens}")

    except Exception as e:
        print(f"Skipping Mistral example: {e}")


if __name__ == "__main__":
    main()

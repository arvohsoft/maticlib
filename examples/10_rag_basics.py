"""
RAG Basics - Embeddings
========================
This example demonstrates how to use Maticlib's unified Embeddings interface
to generate vector representations of text using different providers.
"""

from maticlib.embeddings import OpenAIEmbeddings, GoogleGenAIEmbeddings, MistralEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # 1. Initialize OpenAI Embeddings
    # Make sure OPENAI_API_KEY is set in your environment
    try:
        openai_embed = OpenAIEmbeddings(model="text-embedding-3-small", verbose=True)
        
        # Embed a single query
        query = "What are the core features of Maticlib?"
        vector = openai_embed.embed_query(query)
        print(f"\n[OpenAI] Query Vector (first 5 dims): {vector[:5]}...")
        print(f"[OpenAI] Total Dimensions: {len(vector)}")

    except Exception as e:
        print(f"Skipping OpenAI example: {e}")

    # 2. Initialize Google Gemini Embeddings
    # Make sure GOOGLE_API_KEY is set in your environment
    try:
        google_embed = GoogleGenAIEmbeddings(model="gemini-embedding-001", verbose=True)
        
        # Embed multiple documents in a batch
        docs = [
            "Maticlib is a high-performance Python library for creating AI agents.",
            "It supports multiple providers including OpenAI, Gemini, and Mistral.",
            "The library focuses on type safety and graph-based orchestration."
        ]
        doc_vectors = google_embed.embed_documents(docs)
        
        print(f"\n[Google] Embedded {len(doc_vectors)} documents.")
        print(f"[Google] First Doc Vector (first 5 dims): {doc_vectors[0][:5]}...")
        print(f"[Google] Total Dimensions: {len(doc_vectors[0])}")

    except Exception as e:
        print(f"Skipping Google example: {e}")

    # 3. Initialize Mistral Embeddings
    # Make sure MISTRAL_API_KEY is set in your environment
    try:
        mistral_embed = MistralEmbeddings(model="mistral-embed", verbose=True)
        
        # Embed a single query
        query = "How to integrate API keys?"
        vector = mistral_embed.embed_query(query)
        
        print(f"\n[Mistral] Query Vector (first 5 dims): {vector[:5]}...")
        print(f"[Mistral] Total Dimensions: {len(vector)}")

    except Exception as e:
        print(f"Skipping Mistral example: {e}")

if __name__ == "__main__":
    main()

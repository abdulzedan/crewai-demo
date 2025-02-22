#!/usr/bin/env python
import os

# Set dummy Azure credentials so that the AzureOpenAIEmbeddings don't fail on instantiation.
os.environ.setdefault("AZURE_OPENAI_API_KEY", "dummy")
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "http://dummy")

# Patch the embed_query method on AzureOpenAIEmbeddings to return a dummy embedding.
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings


def dummy_embed_query(self, text):
    return [0.0, 0.1, 0.2]


AzureOpenAIEmbeddings.embed_query = dummy_embed_query

import pytest
from app.services.vector_store import ChromaVectorStore


def test_embed_sample_sentence():
    """
    Test embedding generation for a sample sentence, ensuring the embedding is a non-empty list
    of floats.
    """
    store = ChromaVectorStore(persist_directory=".chroma-local")
    sample_sentence = "This is a test sentence for embedding generation."
    embedding = store.embeddings.embed_query(sample_sentence)

    assert isinstance(embedding, list), "Embedding should be a list of floats"
    assert len(embedding) > 0, "Embedding should not be empty"
    for value in embedding:
        assert isinstance(value, float), "Each element in the embedding should be a float"


if __name__ == "__main__":
    pytest.main()

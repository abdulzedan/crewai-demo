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


def test_local_chroma_store():
    """
    Test that the local Chroma vector store returns a dictionary with a key "documents"
    that contains a list of documents.
    """
    store = ChromaVectorStore(persist_directory=".chroma-local")
    result = store.search_similar("latest research")

    # Assert that the result is a dictionary.
    assert isinstance(result, dict), "Expected result to be a dictionary"

    # Assert that the 'documents' key is present.
    assert "documents" in result, "Expected key 'documents' in result"

    documents = result["documents"]

    # Assert that the 'documents' key contains a list.
    assert isinstance(documents, list), "Expected 'documents' to be a list"


if __name__ == "__main__":
    pytest.main()

#!/usr/bin/env python
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
    # Assert that 'documents' is a list.
    assert isinstance(documents, list), "Expected 'documents' to be a list"


if __name__ == "__main__":
    pytest.main()

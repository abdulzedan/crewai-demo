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

    # Assert that the 'documents' key contains a list.
    assert isinstance(documents, list), "Expected 'documents' to be a list"

    # Optionally, if you expect the list to contain at least one item:
    # assert len(documents) > 0, "Expected at least one document in the local Chroma store"


if __name__ == "__main__":
    pytest.main()

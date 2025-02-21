#!/usr/bin/env python
from app.services.vector_store import ChromaVectorStore

def test_local_chroma_store():
    store = ChromaVectorStore(persist_directory=".chroma-local")
    # Search for a term to see what documents are stored.
    documents = store.search_similar("latest research")
    print("Documents found in local Chroma store:")
    print(documents)
    # This test prints the output for manual inspection.
    
if __name__ == "__main__":
    test_local_chroma_store()

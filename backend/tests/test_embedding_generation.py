#!/usr/bin/env python
from app.services.vector_store import ChromaVectorStore

def test_embed_sample_sentence():
    store = ChromaVectorStore(persist_directory=".chroma-local")
    sample_sentence = "This is a test sentence for embedding generation."
    embedding = store.embeddings.embed_query(sample_sentence)
    print("Embedding for sample sentence:", embedding)
    # Assert the embedding is a non-empty list.
    assert isinstance(embedding, list), "Embedding should be a list of floats"
    assert len(embedding) > 0, "Embedding should not be empty"

if __name__ == "__main__":
    test_embed_sample_sentence()

# test_embedding_generation.py
from backend.app.services.vector_store import ChromaVectorStore

def test_embed_sample_sentence():
    store = ChromaVectorStore()  # uses your configured Azure embeddings
    sample_sentence = "This is a test sentence for embedding generation."
    embedding = store.embeddings.embed_query(sample_sentence)
    print("Embedding for sample sentence:", embedding)
    # Optionally, you can assert properties of the embedding, e.g.:
    assert isinstance(embedding, list), "Embedding should be a list of floats"
    assert len(embedding) > 0, "Embedding should not be empty"

if __name__ == "__main__":
    test_embed_sample_sentence()

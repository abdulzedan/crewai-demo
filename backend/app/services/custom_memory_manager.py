#backend/app/services/custom_memory_manager.py
"""
Example: A "custom memory manager" that an agent can call mid-task 
to store user text and retrieve relevant context from local Chroma.
In practice, you might let your agent call the tools directly, 
or do something more advanced.
"""

from .vector_store import ChromaVectorStore

class CustomMemoryManager:
    def __init__(self, persist_dir="/app/chroma"):
        self.vs = ChromaVectorStore(persist_directory=persist_dir)

    def add_memory(self, text: str):
        self.vs.store_text(text)

    def get_relevant_memories(self, query: str, k=3):
        return self.vs.search_similar(query, k=k)

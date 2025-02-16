# backend/app/services/custom_memory_manager.py

from app.services.vector_store import ChromaVectorStore

class CustomMemoryManager:
    def __init__(self, persist_dir: str = ".chroma-local") -> None:
        self.vector_store = ChromaVectorStore(persist_dir)
        
    def add_memory(self, text: str) -> None:
        try:
            self.vector_store.store_text(text)
        except Exception as e:
            print(f"Memory storage error: {str(e)}")
            raise

    def search_memory(self, query: str):
        try:
            return self.vector_store.search_similar(query)
        except Exception as e:
            print(f"Memory search error: {str(e)}")
            return []

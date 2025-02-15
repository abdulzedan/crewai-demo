from typing import Dict, List
from app.services.vector_store import ChromaVectorStore

class CustomMemoryManager:
    def __init__(self, persist_dir: str = "/app/chroma") -> None:
        self.vs = ChromaVectorStore(persist_directory=persist_dir)

    def add_memory(self, text: str) -> None:
        self.vs.store_text(text)

    def get_relevant_memories(self, query: str, k: int = 3) -> Dict[str, List[str]]:
        return self.vs.search_similar(query_text=query, n_results=k)

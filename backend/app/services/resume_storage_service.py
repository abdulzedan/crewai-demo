from typing import Any, Dict
from app.services.vector_store import ChromaVectorStore
from app.models import StoredResume

class ResumeStorageService:
    def __init__(self, persist_dir: str = "chroma_data") -> None:
        self.vs = ChromaVectorStore(persist_directory=persist_dir)

    def save_resume(self, user_id: int, resume_content: str) -> None:
        StoredResume.objects.create(user_id=user_id, content=resume_content)
        self.vs.store_text(resume_content)

    def find_similar(self, query_text: str) -> Dict[str, Any]:
        return self.vs.search_similar(query_text)

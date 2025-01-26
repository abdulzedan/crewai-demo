"""
A simple example service that stores resumes or user text in DB and in the vector store.
"""
#backend/app/services/resume_storage_service.py
from .vector_store import ChromaVectorStore
from app.models import StoredResume

class ResumeStorageService:
    def __init__(self, persist_dir="chroma_data"):
        self.vs = ChromaVectorStore(persist_directory=persist_dir)

    def save_resume(self, user_id: str, resume_content: str):
        # 1) store in DB
        StoredResume.objects.create(user_id=user_id, content=resume_content)
        # 2) store in vector store for semantic retrieval
        self.vs.store_text(resume_content)

    def find_similar(self, query_text: str):
        return self.vs.search_similar(query_text)

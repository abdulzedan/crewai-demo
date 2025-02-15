import os
import uuid
from dotenv import load_dotenv

from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

load_dotenv()

class ChromaVectorStore:
    def __init__(self, persist_directory: str = "") -> None:
        self.embeddings = AzureOpenAIEmbeddings(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            openai_api_version=os.getenv("AZURE_OPENAI_VERSION", "2024-06-01"),
        )
        self.persist_directory = persist_directory or None
        self.db = Chroma(
            collection_name="collab_writing",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

    def store_text(self, text: str) -> None:
        doc_id = str(uuid.uuid4())
        self.db.add_texts(texts=[text], metadatas=[{"id": doc_id}])
        if self.persist_directory:
            self.db.persist()

    def search_similar(self, query_text: str, n_results: int = 3) -> dict:
        docs = self.db.similarity_search(query_text, k=n_results)
        doc_texts = [doc.page_content for doc in docs]
        return {"documents": [doc_texts]}

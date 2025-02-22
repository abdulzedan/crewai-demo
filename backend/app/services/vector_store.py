import os
import uuid

from dotenv import load_dotenv
from langchain_chroma import Chroma  # Updated package
from langchain_openai import AzureOpenAIEmbeddings

# Load environment variables
load_dotenv()
# Remove any legacy variable to avoid conflicts.
os.environ.pop("OPENAI_API_BASE", None)

# Determine the Azure endpoint using AZURE_OPENAI_ENDPOINT or AZURE_API_BASE.
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_API_BASE", "")
azure_endpoint = endpoint.rstrip("/") if endpoint else None


class ChromaVectorStore:
    def __init__(self, persist_directory: str = "") -> None:
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=azure_endpoint,
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
        )
        self.persist_directory = persist_directory or None
        # Persistence is automatic with the new Chroma
        self.db = Chroma(collection_name="collab_writing", embedding_function=self.embeddings)

    def store_text(self, text: str) -> None:
        doc_id = str(uuid.uuid4())
        try:
            self.db.add_texts(texts=[text], metadatas=[{"id": doc_id}])
        except Exception as e:
            print("Error during store_text:", e)

    def search_similar(self, query_text: str, n_results: int = 3) -> dict:
        try:
            docs = self.db.similarity_search(query_text, k=n_results)
            doc_texts = [doc.page_content for doc in docs]
            return {"documents": [doc_texts]}
        except Exception as e:
            print("Error during search_similar:", e)
            return {"documents": []}

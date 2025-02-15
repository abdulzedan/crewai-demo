from typing import Type
import random
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
from app.services.vector_store import ChromaVectorStore

# ------------------------------
# StoreTextTool
# ------------------------------

class StoreTextInput(BaseModel):
    text: str = Field(..., description="User text to store in Chroma DB")

class StoreTextTool(BaseTool):
    name: str = "store_text_tool"
    description: str = "Store user-provided text into Chroma DB for semantic retrieval"
    args_schema: Type[BaseModel] = StoreTextInput  # Updated: add type annotation
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, text: str) -> str:
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        vs.store_text(text)
        return f"Stored text: {text[:50]}..."

# ------------------------------
# RetrieveTextTool
# ------------------------------

class RetrieveTextInput(BaseModel):
    query: str = Field(..., description="Search query to find relevant text in Chroma DB")

class RetrieveTextTool(BaseTool):
    name: str = "retrieve_text_tool"
    description: str = "Retrieve relevant text from Chroma DB"
    args_schema: Type[BaseModel] = RetrieveTextInput  # Updated: add type annotation
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        results = vs.search_similar(query, n_results=3)
        docs = results.get("documents", [])
        if not docs or not docs[0]:
            return "No similar text found."
        return f"Found {len(docs[0])} doc(s):\n\n" + "\n---\n".join(docs[0])

# ------------------------------
# FindJobsTool
# ------------------------------

class FindJobsInput(BaseModel):
    keyword: str = Field(..., description="Keyword for imaginary job listings")

class FindJobsTool(BaseTool):
    name: str = "find_jobs_tool"
    description: str = "Returns up to 3 imaginary jobs for a given keyword"
    args_schema: Type[BaseModel] = FindJobsInput  # Updated: add type annotation
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, keyword: str) -> str:
        sample_jobs = [
            f"{keyword.capitalize()} Engineer at XYZ Inc. - 3+ years required",
            f"Senior {keyword.capitalize()} Specialist at ABC LLC - Remote possible",
            f"{keyword.capitalize()} Associate at ACME Startup - Great for new grads",
        ]
        random.shuffle(sample_jobs)
        return "\n".join(sample_jobs)

# backend/app/tools/crewai_tools.py

from typing import Type
import random
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
from app.services.vector_store import ChromaVectorStore

# StoreTextTool
class StoreTextInput(BaseModel):
    text: str = Field(..., description="User text to store in Chroma DB")

class StoreTextTool(BaseTool):
    name: str = "store_text_tool"
    description: str = "Store user-provided text into Chroma DB for semantic retrieval"
    args_schema: Type[BaseModel] = StoreTextInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, text: str) -> str:
        try:
            store = ChromaVectorStore(persist_directory=".chroma-local")
            store.store_text(text)
            return "Text stored successfully"
        except Exception as e:
            return f"Storage error: {str(e)}"

# RetrieveTextTool
class RetrieveTextInput(BaseModel):
    query: str = Field(..., description="Search query to find relevant text in Chroma DB")

class RetrieveTextTool(BaseTool):
    name: str = "retrieve_text_tool"
    description: str = "Retrieve relevant text from Chroma DB"
    args_schema: Type[BaseModel] = RetrieveTextInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        try:
            store = ChromaVectorStore(persist_directory=".chroma-local")
            results = store.search_similar(query)
            if results["documents"] and results["documents"][0]:
                return "\n".join(results["documents"][0][:3])
            return "No similar text found."
        except Exception as e:
            return f"Retrieval error: {str(e)}"

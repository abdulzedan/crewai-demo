"""
backend/app/services/tools.py

Applies the Pydantic 2.x fixes: model_config, ClassVar[...] fields.
"""

from typing import ClassVar, Type, Any
import random
from pydantic import BaseModel, Field, ConfigDict

from crewai.tools import BaseTool
from .vector_store import ChromaVectorStore


class StoreTextInput(BaseModel):
    text: str = Field(..., description="User text to store in Chroma DB")


class StoreTextTool(BaseTool):
    """
    Custom tool to store text in local Chroma vector DB.
    """
    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )
    _default_args_schema: ClassVar[Any] = None

    name: ClassVar[str] = "store_text_tool"
    description: ClassVar[str] = "Store user-provided text into Chroma DB"
    args_schema: ClassVar[Type[BaseModel]] = StoreTextInput

    def _run(self, text: str):
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        vs.store_text(text)
        return f"Stored text: {text[:30]}..."


class RetrieveTextInput(BaseModel):
    query: str = Field(..., description="Search query to find relevant text in Chroma DB")


class RetrieveTextTool(BaseTool):
    """
    Custom tool to retrieve text from local Chroma DB.
    """
    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )
    _default_args_schema: ClassVar[Any] = None

    name: ClassVar[str] = "retrieve_text_tool"
    description: ClassVar[str] = "Retrieve relevant text from Chroma DB"
    args_schema: ClassVar[Type[BaseModel]] = RetrieveTextInput

    def _run(self, query: str):
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        results = vs.search_similar(query, n_results=3)
        docs = results["documents"][0] if results and "documents" in results else []
        if not docs:
            return "No similar text found."
        return f"Found {len(docs)} doc(s):\n\n" + "\n---\n".join(docs)


class FindJobsInput(BaseModel):
    keyword: str = Field(..., description="Keyword for imaginary job listings")


class FindJobsTool(BaseTool):
    """
    Imaginary job search tool
    """
    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )
    _default_args_schema: ClassVar[Any] = None

    name: ClassVar[str] = "find_jobs_tool"
    description: ClassVar[str] = "Returns up to 3 imaginary jobs for a given keyword"
    args_schema: ClassVar[Type[BaseModel]] = FindJobsInput

    def _run(self, keyword: str):
        sample_jobs = [
            f"{keyword.capitalize()} Engineer at XYZ Inc. - 3+ years required",
            f"Senior {keyword.capitalize()} Specialist at ABC LLC - Remote possible",
            f"{keyword.capitalize()} Associate at ACME Startup - Great for new grads"
        ]
        random.shuffle(sample_jobs)
        return "\n".join(sample_jobs)

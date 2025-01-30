"""
This module defines custom Tools for CrewAI using Pydantic 2.x–friendly patterns.
- We add explicit type annotations (e.g. name: str, description: str) to match the base class definitions.
- We keep model_config with check_fields=False, extra="allow", arbitrary_types_allowed=True.
- No ClassVar[...] usage, removing conflicts with Pydantic 2.x.
"""

import random
from typing import Type

from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool
from .vector_store import ChromaVectorStore

# --------------------------------------------------------------------------
# 1) StoreTextTool
# --------------------------------------------------------------------------

class StoreTextInput(BaseModel):
    text: str = Field(..., description="User text to store in Chroma DB")


class StoreTextTool(BaseTool):
    """Tool to store text in a local Chroma DB for later semantic retrieval."""

    # ***Important: match the base class's field types.***
    # If BaseTool defines 'name' and 'description' as fields, we override them with the same types.
    name: str = "store_text_tool"
    description: str = "Store user-provided text into Chroma DB for semantic retrieval"
    args_schema: Type[BaseModel] = StoreTextInput

    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )

    def _run(self, text: str) -> str:
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        vs.store_text(text)
        return f"Stored text: {text[:50]}..."


# --------------------------------------------------------------------------
# 2) RetrieveTextTool
# --------------------------------------------------------------------------

class RetrieveTextInput(BaseModel):
    query: str = Field(..., description="Search query to find relevant text in Chroma DB")


class RetrieveTextTool(BaseTool):
    """Tool to retrieve relevant text from a local Chroma DB."""

    name: str = "retrieve_text_tool"
    description: str = "Retrieve relevant text from Chroma DB"
    args_schema: Type[BaseModel] = RetrieveTextInput

    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )

    def _run(self, query: str) -> str:
        vs = ChromaVectorStore(persist_directory=".chroma-local")
        results = vs.search_similar(query, n_results=3)
        docs = results["documents"][0] if results and "documents" in results else []
        if not docs:
            return "No similar text found."
        return f"Found {len(docs)} doc(s):\n\n" + "\n---\n".join(docs)


# --------------------------------------------------------------------------
# 3) FindJobsTool
# --------------------------------------------------------------------------

class FindJobsInput(BaseModel):
    keyword: str = Field(..., description="Keyword for imaginary job listings")


class FindJobsTool(BaseTool):
    """
    An imaginary job search tool to demonstrate Pydantic 2.x usage.
    Returns up to 3 sample jobs for a given keyword.
    """

    name: str = "find_jobs_tool"
    description: str = "Returns up to 3 imaginary jobs for a given keyword"
    args_schema: Type[BaseModel] = FindJobsInput

    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )

    def _run(self, keyword: str) -> str:
        sample_jobs = [
            f"{keyword.capitalize()} Engineer at XYZ Inc. - 3+ years required",
            f"Senior {keyword.capitalize()} Specialist at ABC LLC - Remote possible",
            f"{keyword.capitalize()} Associate at ACME Startup - Great for new grads",
        ]
        random.shuffle(sample_jobs)
        return "\n".join(sample_jobs)


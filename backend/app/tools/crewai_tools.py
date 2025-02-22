from crewai.tools import BaseTool, tool
from pydantic import BaseModel, ConfigDict, Field

from app.services.vector_store import ChromaVectorStore


# Define input schema for storing text.
class StoreTextInput(BaseModel):
    text: str = Field(..., description="User text to store in Chroma DB")


# Custom tool class to store text.
class StoreTextTool(BaseTool):
    name: str = "store_text_tool"
    description: str = "Store user-provided text into Chroma DB for semantic retrieval"
    args_schema: type[BaseModel] = StoreTextInput
    model_config = ConfigDict(
        check_fields=False, extra="allow", arbitrary_types_allowed=True
    )

    def _run(self, text: str) -> str:
        try:
            store = ChromaVectorStore(persist_directory=".chroma-local")
            store.store_text(text)
            return "Text stored successfully"
        except Exception as e:
            return f"Storage error: {str(e)}"


# Function wrapper to register StoreTextTool with CrewAI.
@tool("store_text_tool")
def store_text_tool(text: str) -> str:
    """
    A function wrapper for StoreTextTool.
    This tool stores the provided text into the Chroma vector store for semantic retrieval.
    """
    tool_instance = StoreTextTool()
    return tool_instance._run(text)


# Define input schema for retrieving text.
class RetrieveTextInput(BaseModel):
    query: str = Field(
        ..., description="Search query to find relevant text in Chroma DB"
    )


# Custom tool class to retrieve text.
class RetrieveTextTool(BaseTool):
    name: str = "retrieve_text_tool"
    description: str = "Retrieve relevant text from Chroma DB"
    args_schema: type[BaseModel] = RetrieveTextInput
    model_config = ConfigDict(
        check_fields=False, extra="allow", arbitrary_types_allowed=True
    )

    def _run(self, query: str) -> str:
        try:
            store = ChromaVectorStore(persist_directory=".chroma-local")
            results = store.search_similar(query)
            if results["documents"] and results["documents"][0]:
                return "\n".join(results["documents"][0][:3])
            return "No similar text found."
        except Exception as e:
            return f"Retrieval error: {str(e)}"


# Function wrapper to register RetrieveTextTool with CrewAI.
@tool("retrieve_text_tool")
def retrieve_text_tool(query: str) -> str:
    """
    A function wrapper for RetrieveTextTool.
    This tool retrieves relevant text from the Chroma vector store based on the provided query.
    """
    tool_instance = RetrieveTextTool()
    return tool_instance._run(query)

from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class WebSearchInput(BaseModel):
    query: str = Field(..., description="Search query for web search")

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "Perform a web search and return summarized results."
    args_schema: Type[BaseModel] = WebSearchInput  # Updated: add type annotation
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        # Simulated web search – replace with a call to an actual search API if needed.
        results = f"Simulated web search results for '{query}'."
        return results

# backend/app/tools/aisearch_tool.py

from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class AISearchInput(BaseModel):
    query: str = Field(..., description="Search query for AI research")

class AISearchTool(BaseTool):
    name: str = "ai_search_tool"
    description: str = "Search the web for the latest AI research articles and news"
    args_schema: Type[BaseModel] = AISearchInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, query: str) -> str:
        # For demonstration purposes, we simulate search results.
        simulated_results = (
            f"Simulated search results for query '{query}':\n"
            "1. AI breakthrough in neural network optimization (Source: AI News Daily)\n"
            "2. New AI model achieves state-of-the-art performance (Source: TechReview)\n"
            "3. Latest trends in generative AI discussed at major conference (Source: AI Weekly)"
        )
        return simulated_results

    async def _arun(self, query: str) -> str:
        return self._run(query)

# backend/app/tools/summarize_tool.py


from crewai.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field


class SummarizeInput(BaseModel):
    text: str = Field(..., description="Text to summarize")


class SummarizeTool(BaseTool):
    name: str = "summarize_tool"
    description: str = "Summarize provided text into a concise overview"
    args_schema: type[BaseModel] = SummarizeInput
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, text: str) -> str:
        # For demonstration, we simulate summarization by truncating the text.
        summary = text[:150] + "..." if len(text) > 150 else text
        return f"Summary: {summary}"

    async def _arun(self, text: str) -> str:
        return self._run(text)

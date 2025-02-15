from typing import ClassVar, Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class JobParserInput(BaseModel):
    job_posting: str = Field(..., description="Raw text of a job posting")

class JobParserTool(BaseTool):
    """
    A tool that extracts or highlights required lines from a job posting.
    """
    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
        fields={"_default_args_schema": {"exclude": True}},
    )
    name: ClassVar[str] = "job_parser_tool"
    description: ClassVar[str] = "Useful for analyzing text of a job posting. Extract top skills, etc."
    args_schema: ClassVar[Type[BaseModel]] = JobParserInput

    def _run(self, job_posting: str) -> str:
        lines = job_posting.split('\n')
        highlights = [line.strip() for line in lines if "required" in line.lower() or "must" in line.lower()]
        if not highlights:
            highlights.append("No explicit 'required' lines found.")
        return f"Key lines found: {', '.join(highlights)}"

    async def _arun(self, job_posting: str) -> str:
        return self._run(job_posting)

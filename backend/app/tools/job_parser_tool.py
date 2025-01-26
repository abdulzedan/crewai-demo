"""
backend/app/tools/job_parser_tool.py

Add model_config, ClassVar[...] for Pydantic 2.x compatibility
"""

from typing import ClassVar, Type, Any
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class JobParserInput(BaseModel):
    job_posting: str = Field(..., description="Raw text of a job posting")


class JobParserTool(BaseTool):
    model_config = ConfigDict(
        check_fields=False,
        extra="allow",
        arbitrary_types_allowed=True,
    )
    _default_args_schema: ClassVar[Any] = None

    name: ClassVar[str] = "job_parser_tool"
    description: ClassVar[str] = (
        "Useful for analyzing text of a job posting. Extract top skills, etc."
    )
    args_schema: ClassVar[Type[BaseModel]] = JobParserInput

    def _run(self, job_posting: str):
        lines = job_posting.split('\n')
        highlights = []
        for line in lines:
            if "required" in line.lower() or "must" in line.lower():
                highlights.append(line.strip())

        if not highlights:
            highlights.append("No explicit 'required' lines found.")
        return f"Key lines found: {highlights}"

    async def _arun(self, job_posting: str):
        return self._run(job_posting)

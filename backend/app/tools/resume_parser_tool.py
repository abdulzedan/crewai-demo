from typing import ClassVar, Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class ResumeParserInput(BaseModel):
    resume_text: str = Field(..., description="Raw text of the user resume")

class ResumeParserTool(BaseTool):
    """
    A tool to parse or rewrite a user resume, maybe highlight missing keywords.
    """
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)
    name: ClassVar[str] = "resume_parser_tool"
    description: ClassVar[str] = "Analyzes or rewrites a user resume. May highlight missing keywords."
    args_schema: ClassVar[Type[BaseModel]] = ResumeParserInput

    def _run(self, resume_text: str) -> str:
        if len(resume_text) < 50:
            return "Resume is too short, recommended to expand."
        return "Resume length is decent. Possibly add more job-specific keywords."

    async def _arun(self, resume_text: str) -> str:
        return self._run(resume_text)

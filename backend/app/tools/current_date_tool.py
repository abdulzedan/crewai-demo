# backend/app/tools/current_date_tool.py
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Type

class CurrentDateInput(BaseModel):
    # No inputs required
    pass

class CurrentDateTool(BaseTool):
    name: str = "current_date_tool"
    description: str = "Returns the current date (YYYY-MM-DD)"
    args_schema: Type[BaseModel] = CurrentDateInput

    def _run(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    async def _arun(self) -> str:
        return self._run()

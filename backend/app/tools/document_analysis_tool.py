from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class DocumentAnalysisInput(BaseModel):
    document_text: str = Field(..., description="Text content of the document to analyze")

class DocumentAnalysisTool(BaseTool):
    name: str = "document_analysis_tool"
    description: str = "Analyze a document and extract key insights and summaries."
    args_schema: Type[BaseModel] = DocumentAnalysisInput  # Updated: add type annotation
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, document_text: str) -> str:
        # Simulated analysis – in production, this would call an LLM.
        summary = f"Document summary (first 100 chars): {document_text[:100]}..."
        return summary

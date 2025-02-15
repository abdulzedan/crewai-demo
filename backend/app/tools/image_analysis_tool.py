from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from crewai.tools import BaseTool

class ImageAnalysisInput(BaseModel):
    image_url: str = Field(..., description="URL of the image to analyze")

class ImageAnalysisTool(BaseTool):
    name: str = "image_analysis_tool"
    description: str = "Analyze an image to extract descriptive information using OCR and image recognition."
    args_schema: Type[BaseModel] = ImageAnalysisInput  # Updated: add type annotation
    model_config = ConfigDict(check_fields=False, extra="allow", arbitrary_types_allowed=True)

    def _run(self, image_url: str) -> str:
        # Simulated image analysis – replace with real OCR/image API integration.
        description = f"Simulated analysis for image at {image_url}: A sample descriptive result."
        return description

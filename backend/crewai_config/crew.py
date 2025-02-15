from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from project root (one level above crewai_config)
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Use new variable names per documentation with fallbacks.
AZURE_API_KEY = os.getenv("AZURE_API_KEY", os.getenv("AZURE_OPENAI_API_KEY", ""))
AZURE_API_BASE = os.getenv("AZURE_API_BASE", os.getenv("AZURE_OPENAI_ENDPOINT", ""))
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"))

# According to documentation, the model should be "azure/gpt-4"
LLM_MODEL = "azure/gpt-4o"  # Change to "azure/gpt-4o" if you need that variant

# Build embedder configuration using documented keys.
EMBEDDER_CONFIG = {
    "provider": "openai",
    "config": {
         "api_key": AZURE_API_KEY,
         "api_base": AZURE_API_BASE,
         "api_version": AZURE_API_VERSION,
         "model_name": os.getenv("AZURE_EMBEDDING_MODEL", os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002"))
    }
}

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from app.tools.document_analysis_tool import DocumentAnalysisTool
from app.tools.image_analysis_tool import ImageAnalysisTool
from app.tools.web_search_tool import WebSearchTool
from app.tools.crewai_tools import StoreTextTool, RetrieveTextTool
from pydantic import BaseModel, Field

class AggregatedReport(BaseModel):
    report: str = Field(..., description="Aggregated report combining document, image, and web search analyses.")

@CrewBase
class RAGCrew:
    @agent
    def document_analyzer(self) -> Agent:
        return Agent(
            role="Document Analyzer",
            goal="Extract and summarize key insights from documents.",
            backstory="Expert in textual analysis and summarization.",
            llm=LLM_MODEL,
            tools=[DocumentAnalysisTool(), StoreTextTool(), RetrieveTextTool()],
            memory=True,
            verbose=True
        )

    @agent
    def image_analyzer(self) -> Agent:
        return Agent(
            role="Image Analyzer",
            goal="Analyze images and extract descriptive information.",
            backstory="Expert in computer vision and OCR.",
            llm=LLM_MODEL,
            tools=[ImageAnalysisTool()],
            memory=True,
            verbose=True
        )

    @agent
    def web_searcher(self) -> Agent:
        return Agent(
            role="Web Searcher",
            goal="Fetch and analyze web content based on queries.",
            backstory="Experienced in web scraping and real-time information retrieval.",
            llm=LLM_MODEL,
            tools=[WebSearchTool()],
            memory=True,
            verbose=True
        )

    @task
    def analyze_document(self) -> Task:
        return Task(
            description="Analyze the provided document text and summarize key insights.",
            expected_output="A detailed summary of the document with key points highlighted.",
            agent=self.document_analyzer(),
            async_execution=True,
        )

    @task
    def analyze_image(self) -> Task:
        return Task(
            description="Analyze the image provided via URL and generate a description using OCR and analysis.",
            expected_output="A descriptive summary of the image content.",
            agent=self.image_analyzer(),
            async_execution=True,
        )

    @task
    def web_search(self) -> Task:
        return Task(
            description="Perform a web search based on user query and provide relevant summaries.",
            expected_output="A summary of web search results and relevant information.",
            agent=self.web_searcher(),
            async_execution=True,
        )

    @task
    def aggregate_information(self) -> Task:
        return Task(
            description="Aggregate outputs from document analysis, image analysis, and web search into a comprehensive report.",
            expected_output="A consolidated report combining insights from the document, image, and web search.",
            agent=self.document_analyzer(),
            context=[self.analyze_document(), self.analyze_image(), self.web_search()]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.document_analyzer(),
                self.image_analyzer(),
                self.web_searcher(),
            ],
            tasks=[
                self.analyze_document(),
                self.analyze_image(),
                self.web_search(),
                self.aggregate_information(),
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
            embedder=EMBEDDER_CONFIG
        )

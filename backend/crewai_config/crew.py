# backend/crewai_config/crew.py

from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file from the project root (one level above crewai_config)
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Build the embedder configuration using environment variables.
AZURE_API_KEY = os.getenv("AZURE_API_KEY", os.getenv("AZURE_OPENAI_API_KEY", ""))
AZURE_API_BASE = os.getenv("AZURE_API_BASE", os.getenv("AZURE_OPENAI_ENDPOINT", ""))
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"))

EMBEDDER_CONFIG = {
    "provider": "azure",
    "config": { 
         "api_key": AZURE_API_KEY,
         "api_base": AZURE_API_BASE,
         "api_version": AZURE_API_VERSION,
         "model_name": os.getenv("AZURE_EMBEDDING_MODEL", "text-embedding-ada-002")
    }
}

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from app.tools.aisearch_tool import AISearchTool
from app.tools.summarize_tool import SummarizeTool
from app.tools.crewai_tools import StoreTextTool, RetrieveTextTool

@CrewBase
class LatestAIResearchCrew:
    @agent
    def web_researcher(self) -> Agent:
        return Agent(
            role="Web Researcher",
            goal="Search the web for the latest AI research and tech news.",
            backstory="An expert in scouring online sources for cutting-edge developments in AI and technology.",
            llm="azure/gpt-4o",
            tools=[AISearchTool(), StoreTextTool(), RetrieveTextTool()],
            memory=True,
            verbose=True,
            step_callback=lambda step: print(f"[Web Researcher] {step}")
        )

    @agent
    def aggregator(self) -> Agent:
        return Agent(
            role="Content Aggregator",
            goal="Aggregate and filter search results to highlight key tech insights.",
            backstory="Skilled at synthesizing information into concise summaries.",
            llm="azure/gpt-4o",
            tools=[StoreTextTool(), RetrieveTextTool()],
            memory=True,
            verbose=True,
            step_callback=lambda step: print(f"[Aggregator] {step}")
        )

    @agent
    def synthesizer(self) -> Agent:
        return Agent(
            role="Data Synthesizer",
            goal="Synthesize a comprehensive report from aggregated research.",
            backstory="Experienced in summarizing complex data into clear overviews.",
            llm="azure/gpt-4o",
            tools=[SummarizeTool(), RetrieveTextTool()],
            memory=True,
            verbose=True,
            step_callback=lambda step: print(f"[Synthesizer] {step}")
        )

    @task
    def search_research(self) -> Task:
        return Task(
            description="Search for the latest AI and tech research based on the user's query.",
            expected_output="A list of relevant research articles or findings.",
            agent=self.web_researcher(),
            async_execution=False,
        )

    @task
    def aggregate_research(self) -> Task:
        return Task(
            description="Aggregate and filter the search results to identify the most important insights.",
            expected_output="A curated summary of key findings.",
            agent=self.aggregator(),
            context=[self.search_research()],
            async_execution=False,
        )

    @task
    def synthesize_report(self) -> Task:
        return Task(
            description="Synthesize a final report compiling the aggregated research into a coherent overview.",
            expected_output="A detailed report summarizing the latest in AI and tech.",
            agent=self.synthesizer(),
            context=[self.aggregate_research()],
        )

    @crew
    def crew(self) -> Crew:
        # Disable planning by setting planning to False and providing an empty planning_prompt.
        return Crew(
            agents=[
                self.web_researcher(),
                self.aggregator(),
                self.synthesizer(),
            ],
            tasks=[
                self.search_research(),
                self.aggregate_research(),
                self.synthesize_report(),
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=False,
            planning_prompt=None,  # Explicitly override any default prompt.
            embedder=EMBEDDER_CONFIG  # Supply the embedder config for the API key.
        )

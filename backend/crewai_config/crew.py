# Import storage tools early to register them.
import app.tools.crewai_tools  # This registers store_text_tool and retrieve_text_tool.

import os
import yaml
import copy
from pathlib import Path
from dotenv import load_dotenv
import litellm

# Load .env from the project root (assumed to be three levels up)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Define the configuration directory (inside crewai_config/config)
CONFIG_DIR = Path(__file__).resolve().parent / "config"
if not CONFIG_DIR.exists():
    raise FileNotFoundError(f"Configuration directory not found: {CONFIG_DIR}")

# Load YAML configuration files for agents and tasks.
with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    loaded_agents_config = yaml.safe_load(f)
with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    loaded_tasks_config = yaml.safe_load(f)

from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool
from app.tools.summarize_tool import SummarizeTool
from app.tools.aisearch_tool import AISearchTool
from app.tools.crewai_tools import store_text_tool  # Import function wrapper.

# Create an LLM instance using Azure OpenAI credentials.
llm = LLM(
    model="azure/gpt-4o",  # Adjust as needed.
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION", "2024-06-01")
)

@CrewBase
class LatestAIResearchCrew:
    """
    Crew for research agents.

    Flow:
      1. The Expert Web Researcher uses AISearchTool to fetch live research data.
      2. The Analytical Aggregator compiles and summarizes the research data.
      3. The Store Task saves the aggregated summary into the persistent Chroma vector store.
      4. The Innovative Synthesizer integrates the aggregated insights into a final answer.
    """
    def __init__(self, inputs=None):
        self.inputs = inputs or {}
        print(f"[DEBUG][Crew __init__] Received inputs: {self.inputs}")
        self.agents_config = copy.deepcopy(loaded_agents_config)
        self.tasks_config = copy.deepcopy(loaded_tasks_config)
        print(f"[DEBUG][Crew __init__] Loaded agent keys: {list(self.agents_config.keys())}")
        print(f"[DEBUG][Crew __init__] Loaded task keys: {list(self.tasks_config.keys())}")

    @agent
    def manager(self) -> Agent:
        cfg = self.agents_config.get("manager")
        if cfg is None:
            raise ValueError("Missing 'manager' key in agents.yaml")
        return Agent(
            config=cfg,
            verbose=True,
            llm=llm
        )

    @agent
    def web_researcher(self) -> Agent:
        cfg = self.agents_config.get("web_researcher")
        if cfg is None:
            raise ValueError("Missing 'web_researcher' key in agents.yaml")
        return Agent(
            config=cfg,
            verbose=True,
            llm=llm,
            memory=True,
            tools=[AISearchTool()]
        )

    @agent
    def aggregator(self) -> Agent:
        cfg = self.agents_config.get("aggregator")
        if cfg is None:
            raise ValueError("Missing 'aggregator' key in agents.yaml")
        return Agent(
            config=cfg,
            verbose=True,
            llm=llm,
            memory=True
        )

    @agent
    def synthesizer(self) -> Agent:
        cfg = self.agents_config.get("synthesizer")
        print(f"[DEBUG][synthesizer] Loaded configuration: {cfg}")
        if cfg is None:
            raise ValueError("Missing 'synthesizer' key in agents.yaml")
        return Agent(
            config=cfg,
            verbose=True,
            llm=llm,
            memory=True
        )

    def aggregate_callback(self, task_output):
        """
        Callback for the aggregator task.
        Uses SummarizeTool to condense the research output.
        """
        raw_text = task_output.raw
        summarized = SummarizeTool()._run(raw_text)
        print("[DEBUG][aggregate_callback] Summarized output:", summarized)
        return summarized

    def synthesize_callback(self, task_output):
        """
        Callback for the synthesizer task.
        Processes the aggregated summary into the final answer.
        """
        final_answer = task_output.raw  # Further refinement can be added if needed.
        print("[DEBUG][synthesize_callback] Final synthesized answer:", final_answer)
        return final_answer

    @task
    def research_task(self) -> Task:
        cfg = self.tasks_config.get("research_task")
        if cfg is None:
            raise ValueError("Missing 'research_task' key in tasks.yaml")
        query_input = self.inputs.get("query", "")
        print(f"[DEBUG][research_task] Using query: '{query_input}'")
        return Task(
            config=cfg,
            agent=self.web_researcher(),
            inputs={"query": query_input},
            async_execution=False,
            output_file="research_output.txt"
        )

    @task
    def aggregate_task(self) -> Task:
        cfg = self.tasks_config.get("aggregate_task")
        if cfg is None:
            raise ValueError("Missing 'aggregate_task' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.aggregator(),
            context=[self.research_task()],
            async_execution=False,
            output_file="aggregate_output.txt",
            callback=self.aggregate_callback
        )

    @task
    def store_task(self) -> Task:
        cfg = self.tasks_config.get("store_task")
        if cfg is None:
            raise ValueError("Missing 'store_task' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.aggregator(),
            context=[self.aggregate_task()],
            async_execution=False,
            output_file="stored_output.txt",
            tools=[store_text_tool]  # Explicitly pass the tool function.
        )

    @task
    def synthesize_task(self) -> Task:
        cfg = self.tasks_config.get("synthesize_task")
        if cfg is None:
            raise ValueError("Missing 'synthesize_task' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.synthesizer(),
            context=[self.aggregate_task()],
            async_execution=False,
            output_file="synthesize_output.txt",
            callback=self.synthesize_callback
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.manager(),
                self.web_researcher(),
                self.aggregator(),
                self.synthesizer()
            ],
            tasks=[
                self.research_task(),
                self.aggregate_task(),
                self.store_task(),
                self.synthesize_task()
            ],
            process=Process.sequential,
            verbose=True,
            manager_llm=llm,
            embedder={
                "provider": "azure",
                "config": {
                    "api_key": os.getenv("AZURE_API_KEY"),
                    "api_base": os.getenv("AZURE_API_BASE"),
                    "api_version": os.getenv("AZURE_API_VERSION", "2024-06-01"),
                    "model": os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")
                }
            },
            memory=False,
            full_output=False
        )

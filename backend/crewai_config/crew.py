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

# Load YAML configuration files for agents and tasks
with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    loaded_agents_config = yaml.safe_load(f)
with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    loaded_tasks_config = yaml.safe_load(f)

from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# Create an LLM instance using Azure OpenAI credentials
llm = LLM(
    model="azure/gpt-4o",  # Adjust as needed
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION", "2024-06-01")
)

# Import AISearchTool (which uses Serper and Jina Reader)
from app.tools.aisearch_tool import AISearchTool

@CrewBase
class LatestAIResearchCrew:
    """
    Crew for research agents.

    Flow:
      1. The Expert Web Researcher uses AISearchTool to fetch live search result links and extract content via Jina Reader.
      2. The Analytical Aggregator consolidates these research findings into a structured summary.
      3. The Innovative Synthesizer integrates the aggregated insights into a final, comprehensive answer.
    """
    def __init__(self, inputs=None):
        # Print inputs for debugging
        self.inputs = inputs or {}
        print(f"[DEBUG][Crew __init__] Received inputs: {self.inputs}")
        # Deep copy the configurations so we can inspect them without side effects.
        self.agents_config = copy.deepcopy(loaded_agents_config)
        self.tasks_config = copy.deepcopy(loaded_tasks_config)
        print(f"[DEBUG][Crew __init__] Loaded agent keys: {list(self.agents_config.keys())}")
        print(f"[DEBUG][Crew __init__] Loaded task keys: {list(self.tasks_config.keys())}")

    @agent
    def manager(self) -> Agent:
        """
        Manager agent that routes all queries exclusively to the research process.
        """
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
        """
        Expert Web Researcher that conducts exhaustive online research.
        Utilizes AISearchTool to fetch live search results and extract content.
        """
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
        """
        Analytical Aggregator that compiles and organizes raw research data.
        """
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
        """
        Innovative Synthesizer that transforms aggregated insights into a final answer.
        """
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

    @task
    def research_task(self) -> Task:
        """
        Task for the Expert Web Researcher: Perform an exhaustive online search using AISearchTool.
        Uses the dynamic query provided by the user.
        """
        cfg = self.tasks_config.get("research_task")
        if cfg is None:
            raise ValueError("Missing 'research_task' key in tasks.yaml")
        # Updated: Use "message" from inputs instead of "query"
        query_input = self.inputs.get("message", "")
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
        """
        Task for the Analytical Aggregator: Consolidate raw research data into a structured summary.
        Uses the output from the research task as context.
        """
        cfg = self.tasks_config.get("aggregate_task")
        if cfg is None:
            raise ValueError("Missing 'aggregate_task' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.aggregator(),
            context=[self.research_task()],
            async_execution=False,
            output_file="aggregate_output.txt"
        )

    @task
    def synthesize_task(self) -> Task:
        """
        Task for the Innovative Synthesizer: Integrate aggregated insights into a final comprehensive answer.
        """
        cfg = self.tasks_config.get("synthesize_task")
        if cfg is None:
            raise ValueError("Missing 'synthesize_task' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.synthesizer(),
            context=[self.aggregate_task()],
            async_execution=False,
            output_file="synthesize_output.txt"
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the crew with a sequential process.
        """
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

# crewai_config/crew.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
import litellm

# Enable LiteLLM debug logging (for additional internal info)
litellm._turn_on_debug()

# Load .env from the project root (assumed to be three levels up)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
print(f"[DEBUG] Loaded .env from: {env_path}")

# Define the configuration directory (inside crewai_config/config)
CONFIG_DIR = Path(__file__).resolve().parent / "config"
if not CONFIG_DIR.exists():
    raise FileNotFoundError(f"Configuration directory not found: {CONFIG_DIR}")

# Load the YAML configuration files
with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    loaded_agents_config = yaml.safe_load(f)
with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    loaded_tasks_config = yaml.safe_load(f)

print(f"[DEBUG] Loaded agents configuration: {loaded_agents_config}")
print(f"[DEBUG] Loaded tasks configuration: {loaded_tasks_config}")

# Import CrewAI classes
from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew

# Create an LLM instance using Azure OpenAI credentials from environment variables
llm = LLM(
    model="azure/gpt-4o",  # Adjust as needed (e.g., "azure/gpt-4")
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION", "2024-06-01")
)
print(f"[DEBUG] Created LLM instance: {llm}")

@CrewBase
class LatestAIResearchCrew:
    # Instead of using *args, **kwargs and calling super().__init__,
    # we simply define our own initializer.
    def __init__(self, inputs=None):
        self.agents_config = loaded_agents_config
        self.tasks_config = loaded_tasks_config
        self.inputs = inputs or {}

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
    def generalist(self) -> Agent:
        cfg = self.agents_config.get("generalist")
        if cfg is None:
            raise ValueError("Missing 'generalist' key in agents.yaml")
        # If the system_message contains a placeholder {query}, substitute it.
        if "system_message" in cfg and "{query}" in cfg["system_message"]:
            query_val = self.inputs.get("query", "")
            cfg["system_message"] = cfg["system_message"].format(query=query_val)
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
            memory=True
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
        if cfg is None:
            raise ValueError("Missing 'synthesizer' key in agents.yaml")
        return Agent(
            config=cfg,
            verbose=True,
            llm=llm,
            memory=True
        )

    @task
    def generalist_task(self) -> Task:
        cfg = self.tasks_config.get("generalist_task")
        if cfg is None:
            raise ValueError("Missing 'generalist_task' key in tasks.yaml")
        # Substitute {query} in description if needed.
        if "description" in cfg and "{query}" in cfg["description"]:
            cfg["description"] = cfg["description"].format(query=self.inputs.get("query", ""))
        return Task(
            config=cfg,
            agent=self.generalist(),
            async_execution=False,
            output_file="generalist_output.txt"
        )

    @task
    def research_task(self) -> Task:
        cfg = self.tasks_config.get("research_task")
        if cfg is None:
            raise ValueError("Missing 'research_task' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.web_researcher(),
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
            output_file="aggregate_output.txt"
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
            output_file="synthesize_output.txt"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
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

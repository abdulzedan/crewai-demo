# backend/crewai_config/crew.py

import copy
import os
from pathlib import Path
import yaml
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

# Move these imports to the top to fix E402
from app.tools.aisearch_tool import AISearchTool
from app.tools.crewai_tools import store_text_tool
from app.tools.summarize_tool import SummarizeTool
from app.tools.current_date_tool import CurrentDateTool

# Import for step-level logging
from crewai.agents.parser import AgentAction, AgentFinish
from crewai.agents.crew_agent_executor import ToolResult

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

CONFIG_DIR = Path(__file__).resolve().parent / "config"
if not CONFIG_DIR.exists():
    raise FileNotFoundError(f"Configuration directory not found: {CONFIG_DIR}")

with open(CONFIG_DIR / "agents.yaml", encoding="utf-8") as f:
    loaded_agents_config = yaml.safe_load(f)
with open(CONFIG_DIR / "tasks.yaml", encoding="utf-8") as f:
    loaded_tasks_config = yaml.safe_load(f)

# Create LLM instance
from crewai import LLM

llm = LLM(
    model="azure/gpt-4o",
    api_key=os.getenv("AZURE_API_KEY"),
    base_url=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
)


def format_config(cfg, inputs):
    if isinstance(cfg, dict):
        formatted = {}
        for key, value in cfg.items():
            if isinstance(value, str):
                try:
                    formatted[key] = value.format(**inputs)
                except Exception:
                    formatted[key] = value
            elif isinstance(value, dict):
                formatted[key] = format_config(value, inputs)
            else:
                formatted[key] = value
        return formatted
    return cfg


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
        if "current_date" not in self.inputs:
            self.inputs["current_date"] = CurrentDateTool()._run().strip()
        print(f"[DEBUG][Crew __init__] Received inputs: {self.inputs}")
        self.agents_config = copy.deepcopy(loaded_agents_config)
        self.tasks_config = copy.deepcopy(loaded_tasks_config)
        print(f"[DEBUG][Crew __init__] Loaded agent keys: {list(self.agents_config.keys())}")
        print(f"[DEBUG][Crew __init__] Loaded task keys: {list(self.tasks_config.keys())}")

        # Accumulate logs in markdown
        self.collected_steps = []
        self.final_answer = ""

    def my_step_callback(self, step):
        """
        Produce markdown for each step: AgentAction, AgentFinish, or ToolResult.
        """
        if isinstance(step, AgentAction):
            # Markdown for an Agent Action
            log_entry = f"### **Agent Action**\n```\n{step.text}\n```"
        elif isinstance(step, AgentFinish):
            # Markdown for an Agent Finish
            log_entry = f"### **Agent Finish**\n```\n{step.text}\n```"
        elif isinstance(step, ToolResult):
            # Markdown for a Tool Result
            # step.result is the text from the tool
            log_entry = f"### **Tool Result**\n\n{step.result}"
        else:
            log_entry = f"### **Unknown Step**\n{step}"

        self.collected_steps.append(log_entry)
        print("[DEBUG][step_callback]", log_entry)

    @agent
    def manager(self) -> Agent:
        cfg = self.agents_config.get("manager")
        if cfg is None:
            raise ValueError("Missing 'manager' key in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm)

    @agent
    def web_researcher(self) -> Agent:
        cfg = self.agents_config.get("web_researcher")
        if cfg is None:
            raise ValueError("Missing 'web_researcher' key in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm, memory=True, tools=[AISearchTool()])

    @agent
    def aggregator(self) -> Agent:
        cfg = self.agents_config.get("aggregator")
        if cfg is None:
            raise ValueError("Missing 'aggregator' key in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm, memory=True)

    @agent
    def synthesizer(self) -> Agent:
        cfg = self.agents_config.get("synthesizer")
        print(f"[DEBUG][synthesizer] Loaded configuration: {cfg}")
        if cfg is None:
            raise ValueError("Missing 'synthesizer' key in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm, memory=True)

    def aggregate_callback(self, task_output):
        raw_text = task_output.raw
        summarized = SummarizeTool()._run(raw_text)
        print("[DEBUG][aggregate_callback] Summarized output:", summarized)
        # Return as normal text (or you can convert to markdown if you want)
        # For example:
        return f"**Aggregator Summary**:\n\n{summarized}"

    def synthesize_callback(self, task_output):
        raw_text = task_output.raw
        print("[DEBUG][synthesize_callback] Final synthesized answer:", raw_text)
        # Force final answer to be Markdown
        markdown_final = f"# Final Analysis (Markdown)\n\n{raw_text}\n\n- Date: {self.inputs['current_date']}\n"
        self.final_answer = markdown_final
        return markdown_final

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
            output_file="research_output.txt",
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
            callback=self.aggregate_callback,
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
            tools=[store_text_tool],
        )

    @task
    def synthesize_task(self) -> Task:
        cfg = self.tasks_config.get("synthesize_task")
        if cfg is None:
            raise ValueError("Missing 'synthesizer' key in tasks.yaml")
        return Task(
            config=cfg,
            agent=self.synthesizer(),
            context=[self.aggregate_task()],
            async_execution=False,
            output_file="synthesize_output.txt",
            callback=self.synthesize_callback,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.manager(), self.web_researcher(), self.aggregator(), self.synthesizer()],
            tasks=[self.research_task(), self.aggregate_task(), self.store_task(), self.synthesize_task()],
            process=Process.sequential,
            verbose=True,
            manager_llm=llm,
            embedder={
                "provider": "azure",
                "config": {
                    "api_key": os.getenv("AZURE_API_KEY"),
                    "api_base": os.getenv("AZURE_API_BASE"),
                    "api_version": os.getenv("AZURE_API_VERSION", "2024-06-01"),
                    "model": os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o"),
                },
            },
            memory=False,
            full_output=True,
            step_callback=self.my_step_callback,
        )

# backend/crewai_config/crew.py

import copy
import os
import re
from pathlib import Path
import yaml
from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.crew_agent_executor import ToolResult
from crewai.agents.parser import AgentAction, AgentFinish
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

# Tools
from app.tools.aisearch_tool import AISearchTool
from app.tools.crewai_tools import store_text_tool
from app.tools.current_date_tool import CurrentDateTool

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

CONFIG_DIR = Path(__file__).resolve().parent / "config"
if not CONFIG_DIR.exists():
    raise FileNotFoundError(f"Configuration directory not found: {CONFIG_DIR}")

with open(CONFIG_DIR / "agents.yaml", encoding="utf-8") as f:
    loaded_agents_config = yaml.safe_load(f)
with open(CONFIG_DIR / "tasks.yaml", encoding="utf-8") as f:
    loaded_tasks_config = yaml.safe_load(f)

llm = LLM(
    model="azure/gpt-4o",  # Adjust as needed
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


def extract_search_links(text: str) -> list[dict]:
    # Updated extraction: match lines with format:
    # URL: {url} | Title: {title} | Snippet: {snippet}
    pattern = re.compile(
        r"URL:\s*(https?://[^\s|]+)\s*\|\s*Title:\s*([^|]+)\s*\|\s*Snippet:\s*([^\n]+)",
        re.IGNORECASE,
    )
    links = []
    for match in pattern.finditer(text):
        url, title, snippet = match.groups()
        links.append({"url": url.strip(), "title": title.strip(), "snippet": snippet.strip()})
    return links


@CrewBase
class LatestAIResearchCrew:
    """
    Crew for research agents.
    1. Web researcher fetches data.
    2. Aggregator consolidates in Markdown, removing images.
    3. Store task saves summary.
    4. Synthesizer produces final Markdown answer.
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

        self.collected_steps = []  # Logs in Markdown
        self.final_answer = ""  # Final answer in Markdown
        self.aggregator_links = []  # Will hold extracted search links

    def my_step_callback(self, step):
        if hasattr(step, "result"):
            log_entry = f"Tool Result: {step.result}"
        else:
            timestamp = getattr(step, "timestamp", "Unknown Time")
            task_name = getattr(step, "task_name", "unknown")
            text = getattr(step, "text", "")
            status = getattr(step, "status", "unknown")
            if status == "completed":
                truncated = "\n".join(text.splitlines()[:3])
                log_entry = f'{timestamp}: task_name="{task_name}", task="{truncated}...", status="{status}"'
            else:
                log_entry = f'{timestamp}: task_name="{task_name}", task="{text}", status="{status}"'
        self.collected_steps.append(log_entry)

    @agent
    def manager(self) -> Agent:
        cfg = self.agents_config.get("manager")
        if cfg is None:
            raise ValueError("Missing 'manager' in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm)

    @agent
    def web_researcher(self) -> Agent:
        cfg = self.agents_config.get("web_researcher")
        if cfg is None:
            raise ValueError("Missing 'web_researcher' in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm, memory=True, tools=[AISearchTool()])

    @agent
    def aggregator(self) -> Agent:
        cfg = self.agents_config.get("aggregator")
        if cfg is None:
            raise ValueError("Missing 'aggregator' in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm, memory=True)

    @agent
    def synthesizer(self) -> Agent:
        cfg = self.agents_config.get("synthesizer")
        if cfg is None:
            raise ValueError("Missing 'synthesizer' in agents.yaml")
        cfg = format_config(cfg, self.inputs)
        return Agent(config=cfg, verbose=True, llm=llm, memory=True)

    def aggregate_callback(self, task_output):
        raw_text = task_output.raw
        # Remove image markdown and extraneous image lines.
        text_no_images = re.sub(r"!\[.*?\]\(.*?\)", "", raw_text)
        text_no_images = re.sub(r"Image\s+\d+.*", "", text_no_images)
        # Always read from research_output.txt to force extraction.
        try:
            with open("research_output.txt", encoding="utf-8", errors="ignore") as f:
                research_text = f.read()
            aggregator_links = extract_search_links(research_text)
        except Exception as e:
            aggregator_links = []
        self.aggregator_links = aggregator_links
        return text_no_images

    def synthesize_callback(self, task_output):
        final_markdown = task_output.raw
        if final_markdown.startswith("```") and final_markdown.endswith("```"):
            final_markdown = final_markdown.replace(final_markdown.split("\n")[0] + "\n", "")
            final_markdown = final_markdown.rsplit("\n", 1)[0]
        print("[DEBUG][synthesize_callback] Final synthesized answer:", final_markdown)
        self.final_answer = final_markdown
        return final_markdown

    @task
    def research_task(self) -> Task:
        cfg = self.tasks_config.get("research_task")
        if cfg is None:
            raise ValueError("Missing 'research_task' in tasks.yaml")
        query_input = self.inputs.get("query", "")
        max_links = self.inputs.get("max_links", 3)
        print(f"[DEBUG][research_task] Using query: '{query_input}', max_links: {max_links}")
        return Task(
            config=cfg,
            agent=self.web_researcher(),
            inputs={"query": query_input, "max_links": max_links},
            async_execution=False,
            output_file="research_output.txt",
        )

    @task
    def aggregate_task(self) -> Task:
        cfg = self.tasks_config.get("aggregate_task")
        if cfg is None:
            raise ValueError("Missing 'aggregate_task' in tasks.yaml")
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
            raise ValueError("Missing 'store_task' in tasks.yaml")
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
            raise ValueError("Missing 'synthesizer' in tasks.yaml")
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
            agents=[
                self.manager(),
                self.web_researcher(),
                self.aggregator(),
                self.synthesizer(),
            ],
            tasks=[
                self.research_task(),
                self.aggregate_task(),
                self.store_task(),
                self.synthesize_task(),
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
                    "model": os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o"),
                },
            },
            memory=False,
            full_output=True,
            output_log_file="output_log.txt",
            step_callback=self.my_step_callback,
        )

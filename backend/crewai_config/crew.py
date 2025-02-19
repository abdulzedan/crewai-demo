import os
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

# Ensure these environment variables are set:
# AZURE_API_KEY, AZURE_API_BASE, AZURE_API_VERSION, AZURE_DEPLOYMENT_NAME
EMBEDDER_CONFIG = {
    "provider": "azure",
    "config": {
        "api_key": os.getenv("AZURE_API_KEY"),
        "api_base": os.getenv("AZURE_API_BASE"),
        "api_version": os.getenv("AZURE_API_VERSION", "2024-06-01"),
        "model": os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")
    }
}

@CrewBase
class LatestAIResearchCrew:
    # Manager agent – routes queries only (does not answer directly)
    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config['manager'],
            verbose=True
        )

    # Generalist agent – directly answers simple questions
    @agent
    def generalist(self) -> Agent:
        return Agent(
            config=self.agents_config['generalist'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    # Research pipeline agents
    @agent
    def web_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['web_researcher'],
            verbose=True,
            llm="azure/gpt-4o",
            memory=True
        )

    @agent
    def aggregator(self) -> Agent:
        return Agent(
            config=self.agents_config['aggregator'],
            verbose=True,
            llm="azure/gpt-4o",
            memory=True
        )

    @agent
    def synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['synthesizer'],
            verbose=True,
            llm="azure/gpt-4o",
            memory=True
        )

    # Tasks
    @task
    def generalist_task(self) -> Task:
        return Task(
            description="Answer simple queries directly",
            expected_output="Final Answer: <response>",
            agent=self.generalist(),
            async_execution=False,
            output_file="generalist_output.txt"
        )

    @task
    def research_task(self) -> Task:
        return Task(
            description="Research complex queries using the Web Researcher agent",
            expected_output="Initial research findings",
            agent=self.web_researcher(),
            async_execution=False,
            output_file="research_output.txt"
        )

    @task
    def aggregate_task(self) -> Task:
        return Task(
            description="Aggregate research findings",
            expected_output="Curated summary of key points",
            agent=self.aggregator(),
            context=[self.research_task()],
            async_execution=False,
            output_file="aggregate_output.txt"
        )

    @task
    def synthesize_task(self) -> Task:
        return Task(
            description="Synthesize final answer from aggregated research",
            expected_output="Final Answer: <comprehensive response>",
            agent=self.synthesizer(),
            context=[self.aggregate_task()],
            async_execution=False,
            output_file="synthesize_output.txt"
        )

    @crew
    def crew(self) -> Crew:
        # Instantiate task objects
        generalist_inst = self.generalist_task()
        research_inst = self.research_task()
        aggregate_inst = self.aggregate_task()
        synthesize_inst = self.synthesize_task()

        # Build Crew configuration.
        crew_config = {
            "agents": [
                self.manager().config,
                self.generalist().config,
                self.web_researcher().config,
                self.aggregator().config,
                self.synthesizer().config
            ],
            "tasks": [
                generalist_inst,
                research_inst,
                aggregate_inst,
                synthesize_inst
            ],
            "max_iter": 3,
            "strict_mode": True,
            "ensure_output": True
        }

        return Crew(
            config=crew_config,
            process=Process.hierarchical,
            verbose=True,
            manager_llm="azure/gpt-4o",
            embedder=EMBEDDER_CONFIG,
            memory=False,
            full_output=False,
            task_agent_mapping={
                generalist_inst: [self.generalist()],
                research_inst: [self.web_researcher()],
                aggregate_inst: [self.aggregator()],
                synthesize_inst: [self.synthesizer()]
            }
        )

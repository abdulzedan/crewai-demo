# backend/crewai_config/crew.py

from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import BaseTool

# Import the Tools you already created
from app.services.tools import (
    FindJobsTool,
    StoreTextTool,
    RetrieveTextTool
)

# Import your knowledge source
from .knowledge_sources import job_postings_source

# Define a pydantic model for the final Q&A output
class InterviewQA(BaseModel):
    questions: List[str] = Field(..., description="Interview questions.")
    answers: List[str] = Field(..., description="Corresponding recommended answers.")

# A simple guardrail function: must produce valid JSON that matches InterviewQA
def interview_qa_guardrail(output_str: str):
    """Return (success, data). If success=False, agent will retry."""
    import json
    from json import JSONDecodeError

    try:
        data = json.loads(output_str)
        # The following check is optional if you want to ensure certain fields
        if not isinstance(data.get("questions"), list):
            return (False, "Output JSON has no 'questions' list.")
        if not isinstance(data.get("answers"), list):
            return (False, "Output JSON has no 'answers' list.")
        return (True, data)
    except JSONDecodeError:
        return (False, "Output must be valid JSON with questions/answers.")

@CrewBase
class EnhancedJobApplicationCrew:
    """
    An enhanced version of your JobApplicationCrew with concurrency,
    knowledge usage, memory, guardrails, and optional manager agent.
    """
    agents_config = "crewai_config/agents.yaml"
    tasks_config = "crewai_config/tasks.yaml"

    # Optional: a "manager" agent for hierarchical or planned approach
    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            role="Application Pipeline Manager",
            goal="Coordinate other agents to handle job application tasks.",
            backstory="You oversee the entire process, delegating tasks as needed.",
            llm="gpt-4",  # or any other
            allow_delegation=True,
            verbose=True
        )

    @agent
    def job_researcher(self) -> Agent:
        # Attach the 'find_jobs_tool' plus memory store or retrieval if desired
        return Agent(
            config=self.agents_config["job_researcher"],
            tools=[FindJobsTool(), StoreTextTool(), RetrieveTextTool()],
            llm="gpt-4",
            allow_code_execution=False,
            verbose=True,
            memory=True
        )

    @agent
    def resume_strategist(self) -> Agent:
        # Tools to store or retrieve text from Chroma
        return Agent(
            config=self.agents_config["resume_strategist"],
            tools=[StoreTextTool(), RetrieveTextTool()],
            llm="gpt-4",
            verbose=True,
            allow_code_execution=False,
            memory=True
        )

    @agent
    def interview_coach(self) -> Agent:
        # Tools for retrieving context if needed
        return Agent(
            config=self.agents_config["interview_coach"],
            tools=[RetrieveTextTool()],
            llm="gpt-4",
            verbose=True,
            allow_code_execution=False,
            memory=True
        )

    # tasks
    @task
    def find_jobs(self) -> Task:
        return Task(
            config=self.tasks_config["find_jobs"],
            async_execution=True  # let it run concurrently
        )

    @task
    def store_user_input(self) -> Task:
        return Task(
            config=self.tasks_config["store_user_input"],
            async_execution=True  # let it run concurrently
        )

    @task
    def tailor_resume(self) -> Task:
        # depends on user input + possibly job context
        return Task(
            config=self.tasks_config["tailor_resume"],
            context=[self.find_jobs(), self.store_user_input()]
        )

    @task
    def generate_interview_qa(self) -> Task:
        return Task(
            config=self.tasks_config["generate_interview_qa"],
            context=[self.find_jobs(), self.tailor_resume()],
            guardrail=interview_qa_guardrail,          # ensure valid JSON Q&A
            output_pydantic=InterviewQA                # parse final Q&A to pydantic
        )

    # Finally define the crew
    @crew
    def crew(self) -> Crew:
        """
        If you want a hierarchical approach with a manager agent,
        set `process=Process.hierarchical` and `manager_agent=...`.
        Otherwise keep it sequential + concurrency.
        """
        return Crew(
            agents=[
                self.manager_agent(),     # optional manager
                self.job_researcher(),
                self.resume_strategist(),
                self.interview_coach(),
            ],
            tasks=[
                self.find_jobs(),
                self.store_user_input(),
                self.tailor_resume(),
                self.generate_interview_qa(),
            ],
            process=Process.sequential,
            # For hierarchical flow:
            # process=Process.hierarchical,
            # manager_agent=self.manager_agent(),
            verbose=True,
            memory=True,  # Turn on memory for the entire pipeline
            # Add domain knowledge so agents can consult the stored postings
            knowledge_sources=[job_postings_source],
            # Use an Azure embedder or default OpenAI for storing knowledge
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-ada-002",
                }
            },
            planning=False  # set True if you want dynamic planning
        )

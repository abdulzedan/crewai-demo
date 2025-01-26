#backend/crewai_config/crew.py
"""
Defines the 3-agent pipeline:
1) find_jobs
2) store_user_input (optionally storing user text)
3) tailor_resume
4) generate_interview_qa
"""

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
# Right approach:
from app.services.tools import FindJobsTool, StoreTextTool, RetrieveTextTool


@CrewBase
class JobApplicationCrew:
    agents_config = "crewai_config/agents.yaml"
    tasks_config = "crewai_config/tasks.yaml"

    @agent
    def job_researcher(self) -> Agent:
        # Attach the 'find_jobs_tool' plus memory store or retrieval if desired
        return Agent(
            config=self.agents_config["job_researcher"],
            tools=[FindJobsTool(), StoreTextTool(), RetrieveTextTool()],
            llm="gpt-4",  # Note: Will use Azure behind the scenes if env is set properly
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
        return Task(config=self.tasks_config["find_jobs"])

    @task
    def store_user_input(self) -> Task:
        return Task(config=self.tasks_config["store_user_input"])

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
            context=[self.find_jobs(), self.tailor_resume()]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
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
            verbose=True,
            memory=True,
            embedder={
                "provider": "openai",  # We'll rely on Azure environment
                "config": {
                    "model": "text-embedding-ada-002",
                    "api_key": "",
                    # The other envs are read from environment variables
                }
            }
        )

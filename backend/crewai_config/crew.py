from typing import List
import json

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew

from app.tools.crewai_tools import FindJobsTool, StoreTextTool, RetrieveTextTool
from pydantic import BaseModel, Field

class InterviewQA(BaseModel):
    questions: List[str] = Field(..., description="List of interview questions.")
    answers: List[str] = Field(..., description="Suggested answers.")

def interview_qa_guardrail(output_str: str):
    try:
        parsed = json.loads(output_str)
        if not isinstance(parsed.get("questions"), list):
            return (False, "Missing or invalid 'questions' in output JSON.")
        if not isinstance(parsed.get("answers"), list):
            return (False, "Missing or invalid 'answers' in output JSON.")
        return (True, parsed)
    except json.JSONDecodeError:
        return (False, "Must return valid JSON with 'questions'/'answers'.")

@CrewBase
class JobApplicationCrew:
    @agent
    def job_researcher(self) -> Agent:
        return Agent(
            role="Job Researcher",
            goal="Find relevant job postings and store them or retrieve memory if needed.",
            backstory="Has HR/recruiting background, scanning job boards quickly.",
            llm="gpt-4",
            tools=[FindJobsTool(), StoreTextTool(), RetrieveTextTool()],
            memory=True,
            verbose=True
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            role="Resume Strategist",
            goal="Rewrite or adapt user resumes to match job requirements.",
            backstory="Expert in ATS systems and resume optimization.",
            llm="gpt-4",
            tools=[StoreTextTool(), RetrieveTextTool()],
            memory=True,
            verbose=True
        )

    @agent
    def interview_coach(self) -> Agent:
        return Agent(
            role="Interview Coach",
            goal="Generate interview Q&A based on job context.",
            backstory="20 years experience in interview coaching.",
            llm="gpt-4",
            tools=[RetrieveTextTool()],
            memory=True,
            verbose=True
        )

    @task
    def find_jobs(self) -> Task:
        return Task(
            description="Task: Use the find_jobs_tool to produce a short listing of relevant job postings.",
            expected_output="Up to 3 relevant job listings based on user's input keyword.",
            agent=self.job_researcher(),
            async_execution=True,
        )

    @task
    def store_user_input(self) -> Task:
        return Task(
            description="Task: Store the user's input for future reference, using store_text_tool.",
            expected_output="Confirmation that text was stored in local memory.",
            agent=self.resume_strategist(),
            async_execution=True,
        )

    @task
    def tailor_resume(self) -> Task:
        return Task(
            description="Task: Rewrite or tailor the user's resume to match the found jobs.",
            expected_output="A short, revised resume snippet with relevant keywords.",
            agent=self.resume_strategist(),
            context=[self.find_jobs(), self.store_user_input()]
        )

    @task
    def generate_interview_qa(self) -> Task:
        return Task(
            description=(
                "Task: Generate a short Q&A set (3-5 questions) with recommended answers "
                "based on the job context and user’s updated resume text. Must return "
                "valid JSON with 'questions' and 'answers' arrays."
            ),
            expected_output="JSON with 'questions' and 'answers' arrays",
            agent=self.interview_coach(),
            context=[self.find_jobs(), self.tailor_resume()],
            guardrail=interview_qa_guardrail,
            output_pydantic=InterviewQA,
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
        )

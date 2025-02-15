from celery import shared_task
from crewai_config.crew import JobApplicationCrew  # or EnhancedJobApplicationCrew
from app.models import UserText, CustomUser  # consolidated models

@shared_task
def process_crewai_task(user_input: str, user_id: int = None):
    try:
        user = None
        if user_id is not None:
            user = CustomUser.objects.filter(id=user_id).first()

        # Store initial input in DB
        UserText.objects.create(
            user=user,
            content=f"User input: {user_input}"
        )

        # Kick off the CrewAI pipeline
        crew = JobApplicationCrew().crew()
        result = crew.kickoff(inputs={
            "job_posting": user_input,
            "resume_text": user_input,
            "interview_query": user_input
        })

        # Store final output
        UserText.objects.create(
            user=user,
            content=f"CrewAI result: {result.raw[:500]}..."
        )

        return {
            "status": "completed",
            "result": result.raw[:1000],
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
        }

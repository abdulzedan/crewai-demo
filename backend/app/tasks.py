# backend/app/tasks.py

# Celery has been removed—this is now a plain synchronous function.
from crewai_config.crew import LatestAIResearchCrew
from app.models import UserText, CustomUser

def process_crewai_task(user_input: str, user_id: int = None):
    try:
        user = None
        if user_id is not None:
            user = CustomUser.objects.filter(id=user_id).first()

        # Log the user query into the database.
        UserText.objects.create(
            user=user,
            content=f"User query: {user_input}"
        )

        # Kick off the CrewAI pipeline synchronously.
        crew = LatestAIResearchCrew().crew()
        result = crew.kickoff(inputs={"query": user_input})

        # Log the final output into the database.
        UserText.objects.create(
            user=user,
            content=f"CrewAI research result: {result.raw[:500]}..."
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

from celery import shared_task
from app.models import UserText, CustomUser

@shared_task
def process_chat_task(user_input: str, user_id: int = None):
    try:
        user = None
        if user_id is not None:
            user = CustomUser.objects.filter(id=user_id).first()

        # Store initial chat message in DB
        UserText.objects.create(
            user=user,
            content=f"User input: {user_input}"
        )
        # In this re-designed use-case, task orchestration is handled by CrewAI.
        # This simple task is kept for generic chat messages.
        response_message = f"Received: {user_input}"
        UserText.objects.create(
            user=user,
            content=f"System response: {response_message}"
        )
        return {"status": "completed", "result": response_message}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

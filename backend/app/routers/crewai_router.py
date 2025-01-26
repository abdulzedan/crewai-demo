
#backend/app/routers/crewai_router.py
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from crewai_config.crew import JobApplicationCrew
# from ..models import UserText
from app.models import UserText

# If 'crewai_config' is recognized as a top-level module, do this:
from crewai_config.crew import JobApplicationCrew

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        body = json.loads(request.body or "{}")
        user_input = body.get("message", "")

        # Save user input to DB
        UserText.objects.create(content=f"User input: {user_input}")

        # Run the pipeline
        crew_instance = JobApplicationCrew().crew()
        inputs = {
            "job_posting": user_input, 
            "resume_text": user_input,
            "interview_query": user_input
        }
        output = crew_instance.kickoff(inputs=inputs)

        # Extract each task output
        steps_data = []
        for idx, task_out in enumerate(output.tasks_output):
            # color-coded example
            color = "#FFD700" if idx == 0 else ("#90EE90" if idx == 1 else "#ADD8E6")
            steps_data.append({
                "role": f"Step {idx+1} - {task_out.description}",
                "content": task_out.raw,
                "color": color
            })
        
        # Optionally store final output in DB
        if output.raw:
            UserText.objects.create(content=f"Final Pipeline Output: {output.raw[:150]}")

        return JsonResponse({"steps": steps_data}, status=200)

    return JsonResponse({"error": "Only POST allowed."}, status=405)


urlpatterns = [
    path("", chat_view, name="chat_view"),
]

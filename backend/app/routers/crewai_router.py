# backend/app/routers/crewai_router.py

from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from crewai_config.crew import EnhancedJobApplicationCrew  # changed import
from app.models import UserText


@csrf_exempt
def job_application_pipeline_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed."}, status=405)

    try:
        body = json.loads(request.body or "{}")
        user_input = body.get("message", "")

        # Save user input to DB
        UserText.objects.create(content=f"User input: {user_input}")

        # Run the pipeline
        crew_instance = EnhancedJobApplicationCrew().crew()

        # Provide the user's text to all tasks as needed
        # tasks referencing {job_posting}, {resume_text}, {interview_query}
        inputs = {
            "job_posting": user_input,
            "resume_text": user_input,
            "interview_query": user_input
        }

        output = crew_instance.kickoff(inputs=inputs)
        # The 'output' is a CrewOutput object that includes tasks outputs.

        steps_data = []
        # Loop over each TaskOutput
        for idx, task_out in enumerate(output.tasks_output):
            color = "#FFD700" if idx == 0 else ("#90EE90" if idx == 1 else "#ADD8E6")
            steps_data.append({
                "role": f"Step {idx + 1} - {task_out.description}",
                "content": task_out.raw,
                "color": color
            })

        # If the final output was valid pydantic (InterviewQA), store it or do something:
        final_qa = None
        if output.pydantic is not None:
            final_qa = {
                "questions": output.pydantic.questions,
                "answers": output.pydantic.answers
            }
            UserText.objects.create(content=f"Final Q&A: {final_qa}")

        return JsonResponse({
            "steps": steps_data,
            "final_qa": final_qa
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


urlpatterns = [
    path("", job_application_pipeline_view, name="job_app_pipeline_view"),
]

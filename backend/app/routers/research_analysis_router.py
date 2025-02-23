from django.urls import path
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from crewai_config.crew import LatestAIResearchCrew


class ResearchAnalysisView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=None,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "agentWorkflow": {"type": "array", "items": {"type": "string"}},
                    "finalAnalysis": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "array", "items": {"type": "string"}},
                            "confidence": {"type": "number"},
                        },
                    },
                },
            }
        },
        description="Run the CrewAI workflow and return Markdown logs + final answer.",
    )
    def post(self, request):
        query = request.data.get("query", "")
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            crew_instance = LatestAIResearchCrew(inputs={"query": query})
            crew_obj = crew_instance.crew()
            final_output = crew_obj.kickoff()

            # final_output.result or .final are often the final answer, but we store it in final_answer
            final_answer = crew_instance.final_answer  # Markdown string

            return Response(
                {
                    "agentWorkflow": crew_instance.collected_steps,  # array of Markdown strings
                    "finalAnalysis": {
                        "summary": [final_answer],  # or just final_answer
                        "confidence": getattr(final_output, "confidence", 0.92),
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


urlpatterns = [
    path("", ResearchAnalysisView.as_view(), name="research_analysis"),
]

from django.urls import path
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from app.serializers import AnalysisQuerySerializer
from crewai_config.crew import LatestAIResearchCrew


class ResearchAnalysisView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=AnalysisQuerySerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "agentWorkflow": {"type": "array", "items": {"type": "object"}},
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
        description="Run the CrewAI research workflow with the given query and return structured output including agent logs and final analysis.",
    )
    def post(self, request):
        query = request.data.get("query", "")
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            crew_instance = LatestAIResearchCrew(inputs={"query": query})
            crew_obj = crew_instance.crew()
            # Execute the CrewAI workflow; with full_output=True, kickoff() returns detailed logs and final result.
            final_output = crew_obj.kickoff()

            final_analysis = {
                "summary": final_output.get("result", "").split("\n") if "result" in final_output else [],
                "confidence": final_output.get("confidence", 0.0),
            }

            return Response(
                {
                    "agentWorkflow": final_output.get("steps", []),
                    "finalAnalysis": final_analysis,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


urlpatterns = [
    path("", ResearchAnalysisView.as_view(), name="research_analysis"),
]

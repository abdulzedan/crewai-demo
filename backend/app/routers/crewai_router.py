import os
import traceback
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.serializers import ChatSerializer
from crewai_config.crew import LatestAIResearchCrew
from app.tools.current_date_tool import CurrentDateTool

# Toggle authentication based on an environment variable.
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() in ["true", "1", "yes"]

class SafeDict(dict):
    def __missing__(self, key):
        return ""

class ResearchView(APIView):
    permission_classes = [permissions.IsAuthenticated] if ENABLE_AUTH else [permissions.AllowAny]
    serializer_class = ChatSerializer

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        inputs = serializer.validated_data
        safe_inputs = SafeDict(inputs)
        
        safe_inputs.setdefault("url", "")
        safe_inputs["query"] = safe_inputs.get("message", "")
        safe_inputs["current_date"] = CurrentDateTool()._run().strip()  # Inject current date

        try:
            crew_instance = LatestAIResearchCrew(inputs=safe_inputs)
            crew = crew_instance.crew()
            result = crew.kickoff(inputs=safe_inputs)
        except Exception as e:
            error_trace = traceback.format_exc()
            return Response(
                {"status": "failed", "error": str(e), "trace": error_trace},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        return Response(result, status=status.HTTP_200_OK)

urlpatterns = [
    path("", ResearchView.as_view(), name="research_view"),
]

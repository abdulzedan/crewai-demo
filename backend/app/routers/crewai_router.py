import os
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.serializers import ChatSerializer
from crewai_config.crew import LatestAIResearchCrew

# Toggle authentication based on an environment variable.
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() in ["true", "1", "yes"]

class ResearchView(APIView):
    # If authentication is enabled, use IsAuthenticated; otherwise allow any user.
    permission_classes = [permissions.IsAuthenticated] if ENABLE_AUTH else [permissions.AllowAny]
    serializer_class = ChatSerializer

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        message = serializer.validated_data["message"]

        # Create the crew instance and kickoff with the query input.
        try:
            crew = LatestAIResearchCrew().crew()
            result = crew.kickoff(inputs={"query": message})
        except Exception as e:
            return Response({"status": "failed", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(result, status=status.HTTP_200_OK)

urlpatterns = [
    path("", ResearchView.as_view(), name="research_view"),
]

# backend/app/routers/analysis_router.py

import os

from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers import AnalysisSerializer
from crewai_config.crew import RAGCrew

ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() in ["true", "1", "yes"]


class AnalysisView(APIView):
    # Toggle authentication for analysis as well.
    permission_classes = [permissions.IsAuthenticated] if ENABLE_AUTH else [permissions.AllowAny]

    @extend_schema(
        request=AnalysisSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "report": {
                        "type": "string",
                        "description": "Aggregated report combining document, image, and web search analyses.",
                    }
                },
            }
        },
        description="Analyze a document, image and perform a web search based on the provided parameters.",
    )
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        document_text = data.get("document_text", "")
        image_url = data.get("image_url", "")
        web_query = data.get("web_query", "")

        crew = RAGCrew().crew()
        document_summary = crew.agents[0].tools[0]._run(document_text) if document_text else "No document provided."
        image_summary = crew.agents[1].tools[0]._run(image_url) if image_url else "No image provided."
        web_results = crew.agents[2].tools[0]._run(web_query) if web_query else "No web query provided."

        aggregated_report = (
            f"Document Analysis: {document_summary}\n\n"
            f"Image Analysis: {image_summary}\n\n"
            f"Web Search: {web_results}"
        )
        return Response({"report": aggregated_report}, status=status.HTTP_200_OK)


urlpatterns = [
    path("", AnalysisView.as_view(), name="analysis_view"),
]

# backend/app/routers/research_analysis_router.py

import os
from django.urls import path
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from app.serializers import AnalysisQuerySerializer
from crewai_config.crew import LatestAIResearchCrew
import re  # Import regex module for splitting log entries


class ResearchAnalysisView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=AnalysisQuerySerializer,
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
                    "search_links": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string"},
                                "title": {"type": "string"},
                                "snippet": {"type": "string"},
                                "credibility": {"type": "string"},
                            },
                        },
                    },
                },
            }
        },
    )
    def post(self, request):
        query = request.data.get("query", "")
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            crew_instance = LatestAIResearchCrew(inputs={"query": query})
            crew_obj = crew_instance.crew()
            final_output = crew_obj.kickoff()

            # Read the log file if it exists; fallback to collected_steps if not.
            log_file = "output_log.txt"
            if os.path.exists(log_file):
                # Explicitly use UTF-8 and ignore errors to handle problematic characters
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    log_data = f.read()
                # Split log data into entries using regex that looks for a timestamp at the start of each entry
                agent_workflow = re.split(r"(?=^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:)", log_data, flags=re.MULTILINE)
                agent_workflow = [entry.strip() for entry in agent_workflow if entry.strip()]
            else:
                agent_workflow = crew_instance.collected_steps

            aggregator_links = crew_instance.aggregator_links
            final_answer = crew_instance.final_answer

            return Response(
                {
                    "agentWorkflow": agent_workflow,
                    "finalAnalysis": {
                        "summary": [final_answer],
                        "confidence": getattr(final_output, "confidence", 0.92),
                    },
                    "search_links": aggregator_links,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


urlpatterns = [
    path("", ResearchAnalysisView.as_view(), name="research_analysis"),
]

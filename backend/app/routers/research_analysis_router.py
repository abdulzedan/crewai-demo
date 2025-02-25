# backend/app/routers/research_analysis_router.py

import os
import re

from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

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
        data = request.data
        query = data.get("query", "")
        max_links = data.get("max_links", 3)
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Pass the max_links parameter along with the query
            crew_instance = LatestAIResearchCrew(inputs={"query": query, "max_links": max_links})
            crew_obj = crew_instance.crew()
            final_output = crew_obj.kickoff()

            log_file = "output_log.txt"
            if os.path.exists(log_file):
                with open(log_file, encoding="utf-8", errors="ignore") as f:
                    log_data = f.read()
                raw_entries = re.split(
                    r"(?=^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:)",
                    log_data,
                    flags=re.MULTILINE,
                )
                raw_entries = [entry.strip() for entry in raw_entries if entry.strip()]
                seen = set()
                agent_workflow = []
                for entry in raw_entries:
                    match = re.search(r'task_name="([^"]+)"', entry)
                    content_match = re.search(r'task="([^"]+)"', entry)
                    if match and content_match:
                        key = (match.group(1), content_match.group(1))
                        if key not in seen:
                            seen.add(key)
                            agent_workflow.append(entry)
                    else:
                        agent_workflow.append(entry)
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

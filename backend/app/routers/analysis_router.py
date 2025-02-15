from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from crewai_config.crew import RAGCrew

class AnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Extract inputs for analysis
        document_text = request.data.get("document_text", "")
        image_url = request.data.get("image_url", "")
        web_query = request.data.get("web_query", "")
        
        # Instantiate the RAG crew
        crew = RAGCrew().crew()
        
        # For simplicity, we simulate synchronous tool calls.
        document_summary = (crew.agents[0].tools[0]._run(document_text)
                            if document_text else "No document provided.")
        image_summary = (crew.agents[1].tools[0]._run(image_url)
                         if image_url else "No image provided.")
        web_results = (crew.agents[2].tools[0]._run(web_query)
                       if web_query else "No web query provided.")
        
        aggregated_report = (
            f"Document Analysis: {document_summary}\n\n"
            f"Image Analysis: {image_summary}\n\n"
            f"Web Search: {web_results}"
        )
        return Response({"report": aggregated_report}, status=status.HTTP_200_OK)

urlpatterns = [
    path("", AnalysisView.as_view(), name="analysis_view"),
]

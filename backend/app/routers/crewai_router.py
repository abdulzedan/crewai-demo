# backend/app/routers/crewai_router.py

from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.serializers import ChatSerializer
from app.tasks import process_crewai_task

class ResearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer  # We still use this simple serializer.

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        message = serializer.validated_data["message"]
        user_id = request.user.id  # from JWT or session

        # Call the task function synchronously.
        result = process_crewai_task(user_input=message, user_id=user_id)
        
        return Response(result, status=status.HTTP_200_OK)

urlpatterns = [
    path("", ResearchView.as_view(), name="research_view"),
]

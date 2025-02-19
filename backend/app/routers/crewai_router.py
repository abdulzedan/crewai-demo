# backend/app/routers/crewai_router.py

import os
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.serializers import ChatSerializer
from app.tasks import process_crewai_task

# Toggle authentication based on an environment variable.
# Set ENABLE_AUTH=true in your .env file to require authentication.
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() in ["true", "1", "yes"]

class ResearchView(APIView):
    # If authentication is enabled, use IsAuthenticated; otherwise allow any user.
    permission_classes = [permissions.IsAuthenticated] if ENABLE_AUTH else [permissions.AllowAny]
    serializer_class = ChatSerializer  # We still use this simple serializer.

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        message = serializer.validated_data["message"]
        # Uncomment the following line if you wish to pass the user_id when auth is enabled.
        # user_id = request.user.id if ENABLE_AUTH else None

        # For now, we're passing None for user_id.
        result = process_crewai_task(user_input=message, user_id=None)
        
        return Response(result, status=status.HTTP_200_OK)

urlpatterns = [
    path("", ResearchView.as_view(), name="research_view"),
]

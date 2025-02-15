from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.serializers import ChatSerializer
from app.tasks import process_chat_task

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = serializer.validated_data["message"]
        user_id = request.user.id

        # Call the Celery task (which should run eagerly in tests)
        task = process_chat_task.delay(user_input=message, user_id=user_id)

        return Response({
            "task_id": task.id,
            "status_url": f"/api/tasks/{task.id}/"
        }, status=status.HTTP_202_ACCEPTED)

urlpatterns = [
    path("", ChatView.as_view(), name="chat_view"),
]

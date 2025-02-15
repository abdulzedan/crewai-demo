# backend/app/routers/task_status_router.py

from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from celery.result import AsyncResult

class TaskStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        result = AsyncResult(task_id)
        response_data = {
            "task_id": task_id,
            "state": result.state,
            "result": result.result if result.ready() else None,
        }
        return Response(response_data, status=status.HTTP_200_OK)

urlpatterns = [
    path("<str:task_id>/", TaskStatusView.as_view(), name="task_status_view"),
]

# backend/app/routers/task_status_router.py

import os

from celery.result import AsyncResult
from django.urls import path
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() in ["true", "1", "yes"]


class TaskStatusView(APIView):
    # Toggle auth: if ENABLE_AUTH is true, require authenticated access; else allow any.
    permission_classes = (
        [permissions.IsAuthenticated] if ENABLE_AUTH else [permissions.AllowAny]
    )

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

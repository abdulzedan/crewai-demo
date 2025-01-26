#backend/crewai_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/chat/", include("app.routers.crewai_router")),
]

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crewai_backend.settings")

app = Celery("crewai_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

__all__ = ("app",)

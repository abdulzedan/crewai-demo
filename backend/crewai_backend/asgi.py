# backend/crewai_backend/asgi.py

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crewai_backend.settings")
application = get_asgi_application()

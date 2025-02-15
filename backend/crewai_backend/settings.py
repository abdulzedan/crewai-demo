import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "=v-_mm-p0w%iijguqkl5swhdr+k0qrzy#*tqby7omz64-z(=wn")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
    "rest_framework",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "crewai_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crewai_backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Use the models from app/models.py
AUTH_USER_MODEL = "app.CustomUser"

if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "CrewAI API",
    "DESCRIPTION": "API for AI Agent Workflows",
    "VERSION": "1.0.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-06-01")
# # backend/crewai_backend/settings.py

# import os
# from pathlib import Path
# from datetime import timedelta
# from dotenv import load_dotenv

# # Load environment variables
# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(os.path.join(BASE_DIR, ".env"))

# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "=v-_mm-p0w%iijguqkl5swhdr+k0qrzy#*tqby7omz64-z(=wn")
# DEBUG = os.getenv("DEBUG", "True") == "True"
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# INSTALLED_APPS = [
#     # Django core apps
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     # Local apps
#     "app",
#     # Third-party apps
#     "rest_framework",
#     "drf_spectacular",
# ]

# MIDDLEWARE = [
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
# ]

# ROOT_URLCONF = "crewai_backend.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "crewai_backend.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# # Custom user model from our dedicated models file
# AUTH_USER_MODEL = "app.CustomUser"

# # Security settings for production
# if not DEBUG:
#     SECURE_HSTS_SECONDS = 3600
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True

# # Django REST Framework settings with JWT authentication
# REST_FRAMEWORK = {
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
# }

# SPECTACULAR_SETTINGS = {
#     "TITLE": "CrewAI API",
#     "DESCRIPTION": "API for AI Agent Workflows",
#     "VERSION": "1.0.0",
# }

# # JWT Settings
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
# }

# # Static files configuration
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "static"

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # Celery settings
# CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# # OpenAI and related API settings
# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
# AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-06-01")

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Base directory of your project (assuming settings.py is in crewai_backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the .env file at the project root
load_dotenv(BASE_DIR / ".env")

# SECURITY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "changeme")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Application definition
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

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Custom User Model
AUTH_USER_MODEL = "app.CustomUser"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security settings for production
if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# REST Framework and Schema
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}
SPECTACULAR_SETTINGS = {
    "TITLE": "CrewAI API",
    "DESCRIPTION": "API for RAG and Multi-Modal Analysis",
    "VERSION": "1.0.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# # Celery configuration
# # When running tests, force tasks to run eagerly with an in‑memory broker to avoid connection errors.
# if "test" in sys.argv:
#     CELERY_BROKER_URL = "memory://"
#     CELERY_RESULT_BACKEND = "cache+memory://"
#     CELERY_TASK_ALWAYS_EAGER = True
# else:
#     # Production (or development) Celery settings – adjust these if you have a Redis broker
#     CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
#     CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
#     CELERY_TASK_ALWAYS_EAGER = False

# Azure OpenAI settings (using documented variable names)
AZURE_OPENAI_API_KEY = os.getenv("AZURE_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_API_BASE", "")
AZURE_OPENAI_VERSION = os.getenv("AZURE_API_VERSION", "2024-06-01")
# Optional: For embedding model override
AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

# import os
# from pathlib import Path
# from datetime import timedelta
# from dotenv import load_dotenv

# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(BASE_DIR / ".env")

# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "changeme")
# DEBUG = os.getenv("DEBUG", "True") == "True"
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "memory://")
# CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "cache+memory://")
# CELERY_TASK_ALWAYS_EAGER = True


# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "app",
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

# AUTH_USER_MODEL = "app.CustomUser"

# if not DEBUG:
#     SECURE_HSTS_SECONDS = 3600
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True

# REST_FRAMEWORK = {
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
# }

# SPECTACULAR_SETTINGS = {
#     "TITLE": "CrewAI API",
#     "DESCRIPTION": "API for RAG and Multi-Modal Analysis",
#     "VERSION": "1.0.0",
# }

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
# }

# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "static"
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# if DEBUG:
#     CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "memory://")
#     CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "cache+memory://")
# else:
#     CELERY_BROKER_URL = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
#     CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
# AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-06-01")

#!/usr/bin/env python
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load the .env file from the project root (one level above this file's directory)
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Explicitly set standard OpenAI environment variables from your Azure settings
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_API_KEY", "")
if not os.getenv("OPENAI_API_BASE"):
    os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_API_BASE", "")
if not os.getenv("OPENAI_API_VERSION"):
    os.environ["OPENAI_API_VERSION"] = os.getenv("AZURE_API_VERSION", "2024-06-01")
if not os.getenv("OPENAI_API_TYPE"):
    os.environ["OPENAI_API_TYPE"] = os.getenv("AZURE_API_TYPE", "azure")

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crewai_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

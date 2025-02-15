#!/usr/bin/env python
import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load the .env file from the project root.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# (Optional) Ensure the API key is set.
os.environ.setdefault("AZURE_OPENAI_API_KEY", "9f16cc35170841e593c799f5595ef351")

import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crewai_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

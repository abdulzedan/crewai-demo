#!/usr/bin/env python
import os
# Ensure the OpenAI API key is set early in the process
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

import os
from pathlib import Path

from dotenv import load_dotenv

# Load the .env file from the project root.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path, override=True)

OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT", "")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_VERSION", "")
OPENAI_API_TYPE = os.getenv("AZURE_OPENAI_API_TYPE", "azure")

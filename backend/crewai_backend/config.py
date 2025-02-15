import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH, override=True)

OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT", "")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_VERSION", "")
OPENAI_API_TYPE = os.getenv("AZURE_OPENAI_API_TYPE", "azure")

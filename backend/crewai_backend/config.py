#backend/crewai_backend/config.py:
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", "..", ".env")
load_dotenv(ENV_PATH, override=True)

OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT", "")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_VERSION", "")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")

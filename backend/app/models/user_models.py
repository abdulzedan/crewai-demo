# backend/app/models/user_models.py

from pydantic import BaseModel

class User(BaseModel):
    """
    A simple user model for demonstration of
    CrewAI's output_pydantic usage.
    """
    name: str
    age: int

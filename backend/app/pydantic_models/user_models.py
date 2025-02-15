from pydantic import BaseModel

class User(BaseModel):
    """
    A simple Pydantic user model for CrewAI's output_pydantic usage.
    """
    name: str
    age: int

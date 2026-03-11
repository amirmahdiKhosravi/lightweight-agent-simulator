from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TaskRequest(BaseModel):
    """The incoming payload from the React frontend."""
    task: str = Field(..., description="The user's input task")

class AgentResponse(BaseModel):
    """The structured trace returned to the frontend and saved to SQLite."""
    final_output: str
    execution_steps: List[str]
    tools_used: List[str]
    timestamp: datetime

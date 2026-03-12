"""
Pydantic request/response models shared between the API layer and the agent.
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TaskRequest(BaseModel):
    """Incoming payload from the React frontend."""

    task: str = Field(..., description="The user's input task")


class AgentResponse(BaseModel):
    """Structured execution trace returned to the frontend and persisted to SQLite."""

    final_output: str
    execution_steps: List[str]
    tools_used: List[str]
    timestamp: datetime

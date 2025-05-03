from pydantic import BaseModel
from datetime import datetime


class TaskInRequest(BaseModel):
    title: str
    description: str
    status: str
    priority: int


class TaskInResponse(TaskInRequest):
    id: int
    owner_id: int
    created_at: datetime  # Change from str to datetime

    class Config:
        from_attributes = True  # For SQLAlchemy model conversion
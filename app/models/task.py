from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base, engine


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship with user
    owner = relationship("User", back_populates="tasks")

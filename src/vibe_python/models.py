import datetime
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field
from sqlalchemy import (Column, Integer, String, DateTime, Enum as SQLEnum,
                        ForeignKey)
from sqlalchemy.orm import declarative_base, relationship

# --- Pydantic Models for Configuration Validation ---

class Schedule(BaseModel):
    type: str = "cron"
    expression: str

class OnFailure(BaseModel):
    retries: int = Field(0, ge=0)
    delay_seconds: int = Field(60, ge=0)

class Action(BaseModel):
    type: str
    params: Dict[str, Any] = Field(default_factory=dict)
    description: Optional[str] = None

class Robot(BaseModel):
    robot_name: str
    description: Optional[str] = None
    enabled: bool = True
    schedule: Optional[Schedule] = None
    on_failure: OnFailure = Field(default_factory=OnFailure)
    actions: List[Action]


# --- SQLAlchemy Models for Database Schema ---

Base = declarative_base()

class TaskRun(Base):
    __tablename__ = 'task_runs'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    robot_name: str = Column(String, nullable=False)
    status: str = Column(SQLEnum('Pending', 'Running', 'Success', 'Failed', name='task_status_enum'), nullable=False)
    retry_count: int = Column(Integer, default=0, nullable=False)
    created_at: datetime.datetime = Column(DateTime, default=datetime.datetime.utcnow)
    started_at: Optional[datetime.datetime] = Column(DateTime, nullable=True)
    completed_at: Optional[datetime.datetime] = Column(DateTime, nullable=True)
    result_message: Optional[str] = Column(String, nullable=True)

    logs = relationship("LogEntry", back_populates="task_run")

class LogEntry(Base):
    __tablename__ = 'log_entries'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    task_run_id: int = Column(Integer, ForeignKey('task_runs.id'), nullable=False)
    timestamp: datetime.datetime = Column(DateTime, default=datetime.datetime.utcnow)
    level: str = Column(SQLEnum('INFO', 'WARN', 'ERROR', name='log_level_enum'), nullable=False)
    message: str = Column(String, nullable=False)
    screenshot_path: Optional[str] = Column(String, nullable=True)

    task_run = relationship("TaskRun", back_populates="logs") 
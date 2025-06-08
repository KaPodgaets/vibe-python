import datetime
from contextlib import contextmanager
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base, TaskRun, LogEntry


class DataAccessLayer:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_schema(self):
        """Creates all tables defined in the Base metadata."""
        Base.metadata.create_all(self.engine)
        print("Database schema created successfully.")

    @contextmanager
    def get_session(self) -> Session:
        """Provide a transactional scope around a series of operations."""
        session = self.SessionMaker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_task_run(self, robot_name: str, status: str = 'Pending') -> TaskRun:
        """Creates a new task run record in the database."""
        new_task = TaskRun(robot_name=robot_name, status=status)
        with self.get_session() as session:
            session.add(new_task)
            session.flush()
            session.refresh(new_task)
            return new_task

    def get_task_run(self, task_run_id: int) -> Optional[TaskRun]:
        """Retrieves a single task run by its ID, with its logs."""
        with self.get_session() as session:
            return session.query(TaskRun).filter(TaskRun.id == task_run_id).first()

    def get_latest_task_runs(self, limit: int = 10) -> List[TaskRun]:
        """Retrieves the N most recent task runs."""
        with self.get_session() as session:
            return session.query(TaskRun).order_by(TaskRun.created_at.desc()).limit(limit).all()

    def update_task_run_status(self, task_run_id: int, status: str, result_message: Optional[str] = None):
        """Updates the status and result message of a task run."""
        with self.get_session() as session:
            task = session.query(TaskRun).filter(TaskRun.id == task_run_id).one()
            task.status = status
            if status in ['Running']:
                task.started_at = datetime.datetime.utcnow()
            if status in ['Success', 'Failed']:
                task.completed_at = datetime.datetime.utcnow()
            if result_message:
                task.result_message = result_message

    def increment_task_retry_count(self, task_run_id: int):
        """Increments the retry count for a given task run."""
        with self.get_session() as session:
            task = session.query(TaskRun).filter(TaskRun.id == task_run_id).one()
            task.retry_count += 1

    def add_log_entry(self, task_run_id: int, level: str, message: str, screenshot_path: Optional[str] = None):
        """Adds a new log entry for a specific task run."""
        new_log = LogEntry(
            task_run_id=task_run_id, level=level, message=message, screenshot_path=screenshot_path
        )
        with self.get_session() as session:
            session.add(new_log) 
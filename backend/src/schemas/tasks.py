from ..database.db import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, ForeignKey
from ..models.tasks import Task as TaskModel, TaskEvent as TaskEventModel
import datetime


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now)

    subject: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()

    deadline: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now)

    subtasks: Mapped[JSONB] = mapped_column(JSONB, default={})


class TaskEvent(Base):
    __tablename__ = "task_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    postedAt: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now)

    by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    message: Mapped[str] = mapped_column()


def task_from_schema(task: Task) -> TaskModel:
    task = task.__dict__
    return TaskModel.model_validate(task)


def task_event_from_schema(taskEvent: TaskEvent) -> TaskEventModel:
    taskEvent = taskEvent.__dict__
    return TaskEventModel.model_validate(taskEvent)

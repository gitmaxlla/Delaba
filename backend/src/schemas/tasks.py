from ..database.db import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, ForeignKey
from ..models.tasks import Task as TaskModel, Event as EventModel
import datetime


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    createdAt: Mapped[datetime.datetime] = \
        mapped_column(DateTime, default=func.now())
    modifiedAt: Mapped[datetime.datetime] = \
        mapped_column(DateTime, default=func.now())

    type: Mapped[str] = mapped_column()
    subject: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column(
        ForeignKey("channels.name", ondelete="CASCADE"))

    title: Mapped[str] = mapped_column()
    deadline: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now())

    fileHash: Mapped[str] = mapped_column(nullable=True)
    subtasks: Mapped[JSONB] = mapped_column(JSONB, nullable=True)


def task_from_schema(task: Task) -> TaskModel:
    task = task.__dict__
    return TaskModel.model_validate(task)


# TODO: Events
class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"))

    postedAt: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now())

    by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    message: Mapped[str] = mapped_column()


def event_from_schema(event: Event) -> EventModel:
    event = event.__dict__
    return EventModel.model_validate(event)

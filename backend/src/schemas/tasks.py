from ..database.db import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func, ForeignKey
from ..models.tasks import Task as TaskModel
import datetime

from ..schemas.news import News


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
        ForeignKey("channels.name"))

    title: Mapped[str] = mapped_column()
    deadline: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now())

    fileHash: Mapped[str] = mapped_column(nullable=True)
    subtasks: Mapped[JSONB] = mapped_column(JSONB, nullable=True)

    news: Mapped["News"] = relationship(backref="task",
                                        cascade="all, delete")


def task_from_schema(task: Task) -> TaskModel:
    task = task.__dict__
    return TaskModel.model_validate(task)

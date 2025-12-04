from pydantic import BaseModel
import datetime


class Task(BaseModel):
    id: int
    createdAt: datetime.datetime

    subject: str
    title: str
    deadline: datetime.datetime

    subtasks: dict


class TaskEvent(BaseModel):
    id: int
    by: int
    postedAt: datetime.datetime
    message: str

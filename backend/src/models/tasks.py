from pydantic import BaseModel
import datetime
from typing import List


class Task(BaseModel):
    id: int
    createdAt: datetime.datetime
    modifiedAt: datetime.datetime
    type: str
    channel: str
    subject: str
    title: str

    deadline: datetime.datetime
    subtasks: list | None
    fileHash: str | None


class DocumentTaskCreationRequest(BaseModel):
    subject: str
    title: str
    channel: str
    deadline: datetime.datetime


class TodoTaskCreationRequest(BaseModel):
    subject: str
    title: str
    channel: str
    deadline: datetime.datetime
    subtasks: List[str]


class TaskDeadline(BaseModel):
    deadline: datetime.datetime


class TaskTitle(BaseModel):
    title: str

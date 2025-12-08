from pydantic import BaseModel
import datetime
from typing import List


class Task(BaseModel):
    id: int
    createdAt: datetime.datetime
    modifiedAt: datetime.datetime

    channel: str
    subject: str
    title: str

    deadline: datetime.datetime
    subtasks: dict
    fileHash: str


class Event(BaseModel):
    id: int
    by: int
    postedAt: datetime.datetime
    message: str


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

from pydantic import BaseModel, ConfigDict
import datetime
from typing import List


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class DocumentTaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    title: str
    channel: str
    deadline: datetime.datetime


class TodoTaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    title: str
    channel: str
    deadline: datetime.datetime
    subtasks: List[str]


class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None
    deadline: datetime.datetime

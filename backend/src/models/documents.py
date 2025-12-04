from pydantic import BaseModel
import datetime


class Document(BaseModel):
    id: int
    createdAt: datetime.datetime

    subject: str
    title: str
    deadline: datetime.datetime

    fileHash: dict


class DocumentEvent(BaseModel):
    id: int
    by: int
    postedAt: datetime.datetime
    message: str

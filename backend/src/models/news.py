from pydantic import BaseModel
import datetime


class News(BaseModel):
    id: int
    section: str
    channel: str
    title: str
    by: int
    bound_task_id: int | None

    postedAt: datetime.datetime
    modifiedAt: datetime.datetime
    message: str


class NewsCreationRequest(BaseModel):
    section: str
    channel: str
    title: str
    bound_task_id: int | None
    message: str


class NewsTitle(BaseModel):
    title: str


class NewsMessage(BaseModel):
    message: str


class NewsSection(BaseModel):
    section: str

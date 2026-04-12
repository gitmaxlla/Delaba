from pydantic import BaseModel, ConfigDict
import datetime


class NewsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    channel: str
    section: str
    title: str

    message: str
    bound_task_id: int | None

    postedAt: datetime.datetime
    modifiedAt: datetime.datetime


class News(NewsBase):
    by: int


class NewsCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    channel: str
    section: str
    title: str

    message: str
    bound_task_id: int | None = None


class NewsTitleUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str


class NewsMessageUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str


class NewsSectionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    section: str


class NewsResponse(NewsBase):
    by: str

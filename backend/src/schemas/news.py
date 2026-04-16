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


class NewsUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str | None
    message: str | None
    section: str | None


class NewsResponse(NewsBase):
    by: str


def to_news_response(news: News, by: str) -> NewsResponse:
    return NewsResponse(
        id=news.id,
        channel=news.channel,
        section=news.section,
        title=news.title,
        message=news.message,
        bound_task_id=news.bound_task_id,
        postedAt=news.postedAt,
        modifiedAt=news.modifiedAt,
        by=by,
    )

import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.exceptions import InstanceNotFound
from src.models.channels import Channel

from ..models.news import News as NewsModel
from ..schemas.news import News as NewsSchema
from ..schemas.news import NewsCreate


def add_news(request: NewsCreate, user_id: int, session: Session):
    session.add(
        NewsModel(
            channel=request.channel,
            section=request.section,
            message=request.message,
            bound_task_id=request.bound_task_id,
            by=user_id,
            title=request.title,
        )
    )


def get_news(channel: str, session: Session) -> list[NewsSchema]:
    news: list[NewsSchema] = []

    query = select(NewsModel)
    if channel != "":
        channel_db = session.scalar(select(Channel).where(Channel.name == channel))
        if not channel_db:
            raise InstanceNotFound(f"Channel '{channel}' not found")
        query = query.where(NewsModel.channel == channel)
    news = [NewsSchema.model_validate(x) for x in session.scalars(query).all()]

    return news


def get_news_id(id: int, session: Session) -> NewsSchema:
    news = session.get(NewsModel, id)
    if not news:
        raise InstanceNotFound(f"News (id={id}) not found")
    return NewsSchema.model_validate(news)


def delete_news(id: int, session: Session):
    news = session.get(NewsModel, id)
    session.delete(news)


def change_news_section(id: int, section: str, session: Session):
    news = session.get(NewsModel, id)
    if news:
        news.section = section
        news.modifiedAt = datetime.datetime.now()
    else:
        raise InstanceNotFound(f"News (id={id}) not found")


def change_news_title(id: int, title: str, session: Session):
    news = session.get(NewsModel, id)
    if news:
        news.title = title
        news.modifiedAt = datetime.datetime.now()
    else:
        raise InstanceNotFound(f"News (id={id}) not found")


def change_news_message(id: int, message: str, session: Session):
    news = session.get(NewsModel, id)
    if news:
        news.message = message
        news.modifiedAt = datetime.datetime.now()
    else:
        raise InstanceNotFound(f"News (id={id}) not found")

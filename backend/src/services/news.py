import datetime

from fastapi import HTTPException
from sqlalchemy import select

from ..database import db
from ..models.news import News as NewsModel
from ..schemas.news import News as NewsSchema
from ..schemas.news import NewsCreate


def add_news(request: NewsCreate, user_id: int):
    with db.Session.begin() as session:
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


def get_news(channel) -> list[NewsSchema]:
    news: list[NewsSchema] = []

    query = select(NewsModel)
    if channel != "":
        query = query.where(NewsModel.channel == channel)
    with db.Session() as session:
        news = [NewsSchema.model_validate(x) for x in session.scalars(query).all()]

    return news


def get_news_id(id: int) -> NewsSchema:
    with db.Session() as session:
        news = session.get(NewsModel, id)
        if not news:
            raise HTTPException(status_code=404, detail=f"News (id={id}) not found")
        return NewsSchema.model_validate(news)


def delete_news(id: int):
    with db.Session() as session:
        news = session.get(NewsModel, id)
        session.delete(news)
        session.commit()


def change_news_section(id: int, section: str):
    with db.Session.begin() as session:
        news = session.get(NewsModel, id)
        # TODO: raise exception if not found
        if news:
            news.section = section
            news.modifiedAt = datetime.datetime.now()


def change_news_title(id: int, title: str):
    with db.Session() as session:
        news = session.get(NewsModel, id)
        if news:
            news.title = title
            news.modifiedAt = datetime.datetime.now()
        session.commit()


def change_news_message(id: int, message: str):
    with db.Session() as session:
        news = session.get(NewsModel, id)
        if news:
            news.message = message
            news.modifiedAt = datetime.datetime.now()
        session.commit()

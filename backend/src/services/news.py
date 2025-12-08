from ..database import db
from ..schemas.news import News as NewsSchema, news_from_schema
from typing import List
from sqlalchemy.exc import NoResultFound
from ..models.news import News as NewsModel, NewsCreationRequest
from sqlalchemy import select
from fastapi import HTTPException
from ..models.news import NewsTitle, NewsMessage, NewsSection

import datetime


def add_news(request: NewsCreationRequest, user_id: int):
    with db.Session() as session:
        session.add(NewsSchema(channel=request.channel,
                               section=request.section,
                               message=request.message,
                               bound_task_id=request.bound_task_id,
                               by=user_id,
                               title=request.title))
        session.commit()


def get_news(channel) -> List[NewsModel]:
    news = []

    query = select(NewsSchema)
    if channel != "":
        query = query \
            .where(NewsSchema.channel == channel)
    with db.Session() as session:
        news = session.scalars(query).all()

    return news


def get_news_id(id: int) -> NewsModel:
    with db.Session() as session:
        news = session.get(NewsSchema, id)
        if not news:
            raise HTTPException(status_code=404,
                                detail=f"News (id={id}) not found")
        return news_from_schema(news)


def delete_news(id: int):
    with db.Session() as session:
        news = session.get(NewsSchema, id)
        session.delete(news)
        session.commit()


def change_news_section(id: int, section: str):
    with db.Session() as session:
        news = session.get(NewsSchema, id)
        news.section = section
        news.modifiedAt = datetime.datetime.now()
        session.commit()


def change_news_title(id: int, title: str):
    with db.Session() as session:
        news = session.get(NewsSchema, id)
        news.title = title
        news.modifiedAt = datetime.datetime.now()
        session.commit()


def change_news_message(id: int, message: str):
    with db.Session() as session:
        news = session.get(NewsSchema, id)
        news.message = message
        news.modifiedAt = datetime.datetime.now()
        session.commit()

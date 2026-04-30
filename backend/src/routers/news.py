from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from src.services import news
from src.services.auth import logged_in, owns_channel, moderator, news_id_reachable

from src.schemas.users import User
from src.schemas.news import (
    NewsCreate,
    NewsUpdate,
    NewsResponse,
    to_news_response,
)

from src.services.users import get_user
from src.database.db import get_db

v1_router = APIRouter(prefix="/news", tags=["news"])


@v1_router.post("/")
def add_news(
    request: NewsCreate,
    user: User = Depends(moderator),
    owns_channel: str = Depends(owns_channel),
    db: Session = Depends(get_db),
):

    if owns_channel != "" and owns_channel != request.channel:
        raise HTTPException(403, "Insufficient rights to manage external news.")
    request.channel = owns_channel if owns_channel != "" else request.channel

    news.add_news(request, user.id, db)


@v1_router.get("/")
def get_news(
    user: User = Depends(logged_in), db: Session = Depends(get_db)
) -> list[NewsResponse]:
    fetched_news = news.get_news(user.channel, db)
    response: list[NewsResponse] = []
    for news_ in fetched_news:
        if news_:
            user_ = get_user(news_.by)
            if user_:
                response.append(to_news_response(news_, user_.role))
    return response


@v1_router.get("/{id}")
def get_news_id(
    id: int, _: User = Depends(news_id_reachable), db: Session = Depends(get_db)
):
    return news.get_news_id(id, db)


@v1_router.delete("/{id}")
def delete_task(
    id: int, _: User = Depends(news_id_reachable), db: Session = Depends(get_db)
):
    news.delete_news(id, db)


@v1_router.patch("/{id}")
def update_news_by_id(
    id: int,
    request: NewsUpdate,
    _: User = Depends(news_id_reachable),
    db: Session = Depends(get_db),
):
    if request.title:
        news.change_news_title(id, request.title, db)
    if request.message:
        news.change_news_message(id, request.message, db)
    if request.section:
        news.change_news_section(id, request.section, db)

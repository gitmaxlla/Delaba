from fastapi import APIRouter, Depends, HTTPException
from ..services import news
from ..services.auth import logged_in, owns_channel, moderator, \
                            news_id_reachable

from ..models.users import User
from ..models.news import NewsCreationRequest, NewsMessage, \
                          NewsTitle, NewsSection

v1_router = APIRouter(prefix="/news", tags=["news"])


@v1_router.post("/")
def add_news(request: NewsCreationRequest,
             user: User = Depends(moderator),
             owns_channel: str = Depends(owns_channel)):

    if owns_channel != "" and owns_channel != request.channel:
        raise HTTPException(403,
                            "Insufficient rights to manage external news.")
    request.channel = owns_channel if owns_channel != "" \
        else request.channel

    news.add_news(request, user.id)


@v1_router.get("/")
def get_news(user: User = Depends(logged_in)):
    return news.get_news(user.channel)


@v1_router.get("/{id}")
def get_news_id(id: int,
                permitted: User = Depends(news_id_reachable)):
    return news.get_news_id(id)


@v1_router.delete("/{id}")
def delete_task(id: int,
                permitted: User = Depends(news_id_reachable)):
    news.delete_news(id)


@v1_router.patch("/{id}/title")
def change_news_title(id: int,
                      request: NewsTitle,
                      permitted: User = Depends(news_id_reachable)):
    news.change_news_title(id, request.title)


@v1_router.patch("/{id}/message")
def change_news_message(id: int,
                        request: NewsMessage,
                        permitted: User = Depends(news_id_reachable)):
    news.change_news_message(id, request.message)


@v1_router.patch("/{id}/section")
def change_news_section(id: int,
                        request: NewsSection,
                        permitted: User = Depends(news_id_reachable)):
    news.change_news_section(id, request.section)

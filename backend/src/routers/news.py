from fastapi import APIRouter
from ..services import news


v1_router = APIRouter(prefix="/news", tags=["news"])


@v1_router.get("/")
def get_all_news():
    news.get_all_news()


@v1_router.post("/")
def add_news():
    news.add_news()


@v1_router.get("/{id}")
def get_news(id):
    news.get_news(id)


@v1_router.delete("/{id}")
def delete_news(id):
    news.delete_news(id)


@v1_router.patch("/{id}/heading")
def change_news_heading(id):
    news.change_news_heading(id)


@v1_router.patch("/{id}/body")
def change_news_body(id):
    news.change_news_body(id)

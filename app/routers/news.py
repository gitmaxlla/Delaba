from fastapi import APIRouter
from ..services import news_service


v1_router = APIRouter(prefix="/news", tags=["news"])


@v1_router.get("/")
def get_all_news():
    news_service.get_all_news()


@v1_router.put("/")
def add_news():
    news_service.add_news()


@v1_router.get("/{id}")
def get_news(id):
    news_service.get_news(id)


@v1_router.delete("/{id}")
def delete_news(id):
    news_service.delete_news(id)


@v1_router.put("/{id}")
def update_news(id):
    news_service.update_news(id)


@v1_router.patch("/{id}/heading")
def change_news_heading(id):
    news_service.change_news_heading(id)


@v1_router.patch("/{id}/body")
def change_news_body(id):
    news_service.change_news_body(id)

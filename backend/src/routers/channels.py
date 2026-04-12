from fastapi import APIRouter, Depends
from typing import List

from src.schemas.users import User
from src.schemas.news import News
from src.schemas.tasks import Task
from src.schemas.channels import ChannelCreate

from src.services.auth import admin, logged_in
from src.services.channels import (
    users_by_channel as get_users_by_channel,
    tasks_by_channel as get_tasks_by_channel,
    news_by_channel as get_news_by_channel,
    get_channels as get_channels_service,
    create_channel as create_channel_service,
    delete_channel as delete_channel_service,
)


v1_router = APIRouter(prefix="/channels", tags=["channels"])


@v1_router.get("/users")
def users_by_channel(channel: str, _: User = Depends(admin)) -> List[User]:
    return get_users_by_channel(channel)


@v1_router.get("/news")
def news_by_channel(channel: str, _: User = Depends(admin)) -> List[News]:
    return get_news_by_channel(channel)


@v1_router.get("/tasks")
def tasks_by_channel(channel: str, _: User = Depends(admin)) -> List[Task]:
    return get_tasks_by_channel(channel)


@v1_router.get("/")
def get_channels(user: User = Depends(logged_in)) -> List[str]:
    return get_channels_service(user)


@v1_router.post("/")
def create_channel(channel: ChannelCreate, _: User = Depends(admin)):
    return create_channel_service(channel)


@v1_router.delete("/")
def delete_channel(channel: ChannelCreate, _: User = Depends(admin)):
    # raise HTTPException(403, "Removing root channel is not allowed.")
    delete_channel_service(channel)
    return delete_channel_service(channel)

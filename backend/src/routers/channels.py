from fastapi import APIRouter, Depends
from typing import List

from ..models.users import User
from ..models.news import News
from ..models.tasks import Task

from ..models.channels import ChannelRequest
from ..services.auth import admin
from ..services.channels import users_by_channel as get_users_by_channel, \
                              tasks_by_channel as get_tasks_by_channel, \
                              news_by_channel as get_news_by_channel, \
                              get_channels as get_channels_service, \
                              create_channel as create_channel_service, \
                              delete_channel as delete_channel_service

v1_router = APIRouter(prefix="/channels", tags=["channels"])


@v1_router.get("/users")
def users_by_channel(channel: str,
                     admin: User = Depends(admin)) -> List[User]:
    return get_users_by_channel(channel)


@v1_router.get("/news")
def news_by_channel(channel: str,
                    admin: User = Depends(admin)) -> List[News]:
    return get_news_by_channel(channel)


@v1_router.get("/tasks")
def tasks_by_channel(channel: str,
                     admin: User = Depends(admin)) -> List[Task]:
    return get_tasks_by_channel(channel)


@v1_router.get("/")
def get_channels(admin: User = Depends(admin)) -> List[str]:
    return get_channels_service()


@v1_router.post("/")
def create_channel(channel: ChannelRequest,
                   admin: User = Depends(admin)):
    return create_channel_service(channel)


@v1_router.delete("/")
def delete_channel(channel: ChannelRequest,
                   admin: User = Depends(admin)):
    return delete_channel_service(channel)

from fastapi import APIRouter, HTTPException
from ..models.channels import ChannelRequest
from sqlalchemy import select

from ..models.users import User as UserModel
from ..models.tasks import Task as TaskModel
from ..models.news import News as NewsModel

from ..schemas.users import User as UserSchema
from ..schemas.news import News as NewsSchema
from ..schemas.tasks import Task as TaskSchema

from typing import List
from ..database import db
from ..schemas.channels import Channel

v1_router = APIRouter(prefix="/channels", tags=["channels"])


def users_by_channel(channel: str) -> List[UserModel]:
    users = []

    with db.Session() as session:
        users = session.scalars(select(UserSchema)
                                .where(UserSchema.channel == channel)).all()

    return users


def news_by_channel(channel: str) -> List[NewsModel]:
    news = []

    with db.Session() as session:
        news = session.scalars(select(NewsSchema)
                               .where(NewsSchema.channel == channel)).all()

    return news


def tasks_by_channel(channel: str) -> List[TaskModel]:
    tasks = []

    with db.Session() as session:
        tasks = session.scalars(select(TaskSchema)
                                .where(TaskSchema.channel == channel)).all()

    return tasks


def get_channels() -> List[str]:
    with db.Session() as session:
        channels = session.query(Channel).all()
    return [channel.name for channel in channels]


def create_channel(request: ChannelRequest):
    with db.Session() as session:
        session.add(Channel(name=request.channel))
        session.commit()


def delete_channel(request: ChannelRequest):
    if request.channel == "":
        raise HTTPException(403, "Removing root channel is not allowed.")

    with db.Session() as session:
        channel = session.get(Channel, request.channel)
        session.delete(channel)
        session.commit()

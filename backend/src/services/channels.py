from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.schemas.channels import ChannelCreate
from src.models.users import User as UserModel
from src.models.tasks import Task as TaskModel
from src.models.news import News as NewsModel
from src.schemas.users import User as UserSchema
from src.schemas.news import News as NewsSchema
from src.schemas.tasks import Task as TaskSchema
from src.core.permissions import has_admin_rights
from src.core.exceptions import RootEntityViolationError
from src.database import db
from src.models.channels import Channel


def users_by_channel(channel: str) -> list[UserSchema]:
    users: list[UserSchema] = []

    with db.Session.begin() as session:
        users = [
            UserSchema.model_validate(x)
            for x in list(
                session.scalars(
                    select(UserModel).where(UserModel.channel == channel)
                ).all()
            )
        ]

    return users


def news_by_channel(channel: str) -> list[NewsSchema]:
    news = []

    with db.Session() as session:
        news = [
            NewsSchema.model_validate(x)
            for x in session.scalars(
                select(NewsModel).where(NewsModel.channel == channel)
            ).all()
        ]

    return news


def tasks_by_channel(channel: str) -> list[TaskSchema]:
    tasks = []

    with db.Session() as session:
        tasks = [
            TaskSchema.model_validate(x)
            for x in session.scalars(
                select(TaskModel).where(TaskModel.channel == channel)
            ).all()
        ]

    return tasks


def get_channels(user: UserSchema, session: Session) -> list[str]:
    if has_admin_rights(user.permissions):
        channels = session.query(Channel).all()
        return [channel.name for channel in channels]

    return [user.channel]


def create_channel(request: ChannelCreate):
    with db.Session.begin() as session:
        session.merge(Channel(name=request.channel))


def delete_channel(request: ChannelCreate):
    if request.channel == "":
        raise RootEntityViolationError("Removing root channel is not allowed.")

    with db.Session.begin() as session:
        channel = session.get(Channel, request.channel)
        session.delete(channel)

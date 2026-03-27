import time
import datetime
import random

from faker import Faker
from fastapi import APIRouter, Response

from ..services.auth import set_tokens, TokenPayload
from ..services.news import add_news
from ..services.users import add_user, Permissions
from ..services.channels import create_channel, ChannelRequest
from ..services.users import ban_user, make_moderator, unban_user, \
                             make_admin, make_default, get_all_users
from ..services.tasks import add_document_task, add_todo_task, \
                             TodoTaskCreationRequest, \
                             DocumentTaskCreationRequest

from ..models.news import NewsCreationRequest
from ..database import db


fake = Faker()
v1_router = APIRouter(prefix="/mock", tags=["mock"])


def mock_data():
    CHANNELS=10
    USERS=50
    TODOS=150
    NEWS=50

    channels = [" ".join(fake.words(3)) for i in range(CHANNELS)]
    subjects = [" ".join(fake.words(2)) for i in range(TODOS // 10)]
    sections = [fake.word() for i in range(5)]
    users = get_all_users()

    for channel in channels:
        create_channel(ChannelRequest(channel=channel))

    for i in range(USERS):
        channel = random.choice(channels)
        add_user(fake.email(), fake.name(),
                 channel, Permissions.VIEW_CHANNEL)

    for i in range(TODOS):
        add_todo_task(TodoTaskCreationRequest(
            subject=random.choice(subjects), title=" ".join(fake.words(5)),
            channel=random.choice(channels),
            deadline=fake.date_time_this_year(after_now=True), subtasks=fake.words(3)
        ))

    for i in range(NEWS):
        user = random.choice(users)
        add_news(NewsCreationRequest(section=random.choice(sections), 
                                     channel=user.channel, title=" ".join(fake.words(5)), 
                                     message=fake.text(100)), user.id)


@v1_router.post("/sample", tags=["mock"])
async def insert_mock_data():
    mock_data()

@v1_router.post("/drop", tags=["mock"])
async def drop_database():
    db.drop_all()

@v1_router.post("/token", tags=["mock"])
async def mock_token(response: Response):
    set_tokens(TokenPayload(0), response)


@v1_router.post("/ban", tags=["mock"])
async def mock_ban():
    await ban_user(0)


@v1_router.post("/unban", tags=["mock"])
async def mock_unban():
    await unban_user(0)


@v1_router.post("/moderator", tags=["mock"])
async def mock_moderator():
    await make_moderator(0)


@v1_router.post("/viewer", tags=["mock"])
async def mock_viewer():
    await make_default(0)


@v1_router.post("/admin", tags=["mock"])
async def mock_admin():
    await make_admin(0)

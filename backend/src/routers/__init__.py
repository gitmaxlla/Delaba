from fastapi import APIRouter
from . import users, tasks, news, channels, mock
from ..services import auth

from datetime import datetime
import os

start_timestamp = datetime.now()

router = APIRouter()

v1 = APIRouter(prefix="/v1")
v1.include_router(users.v1_router)
v1.include_router(tasks.v1_router)
v1.include_router(news.v1_router)
v1.include_router(auth.v1_router)
v1.include_router(channels.v1_router)

if os.getenv("INCLUDE_MOCK_ROUTES") == "true":
    v1.include_router(mock.v1_router)


@router.get("/", tags=["root"])
async def about():
    """
    Check API availability and supported versions
    """

    now_timestamp = datetime.now()
    return {"message": "Welcome to Delaba project API!",
            "versions": get_version_list(),
            "started": start_timestamp,
            "now": now_timestamp,
            "uptime": (now_timestamp - start_timestamp)}

router.include_router(v1)


def get_version_list():
    return ["v1"]

from fastapi import APIRouter
from . import users, tasks, news, documents
from ..services import auth

from datetime import datetime
start_timestamp = datetime.now()

router = APIRouter()

v1 = APIRouter(prefix="/v1")
v1.include_router(users.v1_router)
v1.include_router(tasks.v1_router)
v1.include_router(news.v1_router)
v1.include_router(documents.v1_router)


@v1.post("/auth", tags=["users"])
async def authenticate():
    auth.authenticate()


@router.get("/health")
async def healthcheck():
    now_timestamp = datetime.now()
    return {"started": start_timestamp,
            "now": now_timestamp,
            "uptime": (now_timestamp - start_timestamp)}

router.include_router(v1)


def get_version_list():
    return ["v1"]

from fastapi import APIRouter
from app.routers import users, tasks, news, documents
from app.services import auth_service


router = APIRouter()

v1 = APIRouter(prefix="/v1")
v1.include_router(users.v1_router)
v1.include_router(tasks.v1_router)
v1.include_router(news.v1_router)
v1.include_router(documents.v1_router)


@v1.post("/auth", tags=["users"])
async def authenticate():
    auth_service.authenticate()

router.include_router(v1)


def get_version_list():
    return ["v1"]

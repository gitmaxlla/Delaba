from fastapi import FastAPI, APIRouter
from app.routers import users, tasks, news, documents
from app.services import auth_service


app = FastAPI()

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users.v1_router)
v1_router.include_router(tasks.v1_router)
v1_router.include_router(news.v1_router)
v1_router.include_router(documents.v1_router)


@v1_router.post("/auth", tags=["users"])
async def authenticate():
    auth_service.authenticate()


app.include_router(v1_router)


@app.get("/", tags=["app"])
async def about():
    """
    Check API availability and supported versions
    """

    return {"message": "Welcome to Delaba project API!",
            "versions": ["v1"]}

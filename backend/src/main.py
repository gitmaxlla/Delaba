import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.routers.root import router
from src.database import db, obj
from src.internal.setup import manager

from src.models.news import News
from src.models.users import User
from src.models.tasks import Task
from src.models.channels import Channel

from src.core.security import RateLimiter
from src.core.config import DEV_MODE, ALLOWED_HOSTNAME, LogFilter


# For type checkers not to mark schemas unused
INCLUDE_SCHEMAS = News, User, Task, Channel


@asynccontextmanager
async def lifespan(_: FastAPI):
    obj.create_default_bucket()
    db.create_all()
    manager.init_app()

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://127.0.0.1"]
    if DEV_MODE
    else ["" if ALLOWED_HOSTNAME is None else ALLOWED_HOSTNAME],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.getLogger("uvicorn.access").addFilter(LogFilter())


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.client is not None:
        request_address = request.client.host
        retry_after = RateLimiter().exceeded(request_address)
        if retry_after:
            return Response(status_code=429, headers={"Retry-After": str(retry_after)})

    response = await call_next(request)
    return response


app.include_router(router)

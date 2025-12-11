from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .routers import router
from .database import db
from .services.users import create_admin_user

from .core.security import RateLimiter

from .schemas.news import News
from .schemas.users import User
from .schemas.tasks import Task
from .schemas.channels import Channel

from .routers.mock import mock_data
import os

News, User, Task, Channel

if os.getenv("ENABLE_MOCKING") == "true":
    db.drop_all()

db.create_all()

create_admin_user()

if os.getenv("ENABLE_MOCKING") == "true":
    mock_data()

app = FastAPI()
limiter = RateLimiter()


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    request_address = request.client.host
    retry_after = limiter.exceeded(request_address)
    if retry_after:
        return Response(status_code=429,
                        headers={"Retry-After": str(retry_after)})

    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router)

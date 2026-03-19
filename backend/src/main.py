from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routers import router
from .database import db
from .services.users import create_admin_user

from .core.security import RateLimiter

from .schemas.news import News
from .schemas.users import User
from .schemas.tasks import Task
from .schemas.channels import Channel

from .core.config import DEV_MODE, ALLOWED_HOSTNAME, LogFilter
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    News, User, Task, Channel
    db.create_all()
    create_admin_user()
    
    yield

app = FastAPI(lifespan=lifespan)
logging.getLogger("uvicorn.access").addFilter(LogFilter())

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    request_address = request.client.host
    retry_after = RateLimiter().exceeded(request_address)
    if retry_after:
        return Response(status_code=429,
                        headers={"Retry-After": str(retry_after)})

    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if DEV_MODE else ALLOWED_HOSTNAME],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router)

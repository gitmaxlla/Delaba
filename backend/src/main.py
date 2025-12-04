from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from .routers import router, get_version_list
from .database import db
from .services.users import add_an_user

from .core.security import RateLimiter

from .schemas.news import News
from .schemas.users import User
from .schemas.documents import Document, DocumentEvent
from .schemas.tasks import Task, TaskEvent


News, User, DocumentEvent, Document, Task, TaskEvent
db.drop_all()
db.create_all()


first_init_token = add_an_user("First", "University1-Group-Subject-Year-Semester")["init_token"]
add_an_user("Second", "University2-Group-Subject-Year-Semester")

print(first_init_token)

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
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router)


@app.get("/", tags=["app"])
async def about():
    """
    Check API availability and supported versions
    """

    return {"message": "Welcome to Delaba project API!",
            "versions": get_version_list()}

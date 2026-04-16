import datetime
import hashlib
from typing import Annotated

import fleep
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from src.core.config import FILE_UPLOAD_LIMIT_BYTES
from src.database.obj import client as storage
from src.database.obj import get_default_bucket
from src.schemas.tasks import (
    DocumentTaskCreate,
    Task,
    TaskUpdate,
    TodoTaskCreate,
)
from src.schemas.users import User
from src.services import tasks
from src.services.auth import logged_in, owns_channel, task_id_reachable

v1_router = APIRouter(prefix="/tasks", tags=["tasks"])


@v1_router.get("/")
def get_tasks(user: User = Depends(logged_in)):
    return tasks.get_tasks(user.channel)


@v1_router.post("/todo")
def add_todo_task(request: TodoTaskCreate, owns_channel: str = Depends(owns_channel)):
    if owns_channel != "" and owns_channel != request.channel:
        raise HTTPException(403, "Insufficient rights to manage external channels.")
    request.channel = owns_channel if owns_channel != "" else request.channel

    return tasks.add_todo_task(request)


@v1_router.post("/document")
async def add_document_task(
    file: UploadFile,
    title: Annotated[str, Form()],
    subject: Annotated[str, Form()],
    deadline: Annotated[datetime.datetime, Form()],
    channel: Annotated[str, Form()] = "",
    owns_channel: str = Depends(owns_channel),
):
    if not file.size:
        raise HTTPException(422, "File size cannot be read by the server.")
    if file.size and file.size > FILE_UPLOAD_LIMIT_BYTES:
        raise HTTPException(413, "File upload limit has been exceeded (20 MB).")

    request = DocumentTaskCreate(
        subject=subject, title=title, channel=channel, deadline=deadline
    )

    if owns_channel != "" and owns_channel != channel:
        raise HTTPException(403, "Insufficient rights to manage external channels.")
    request.channel = owns_channel if owns_channel != "" else request.channel

    hasher = hashlib.md5()
    pdf_header_present = False

    while data := await file.read(2048):
        if not pdf_header_present:
            info = fleep.get(data)
            if not info.extension_matches("pdf"):
                raise HTTPException(400, "No PDF header on upload.")
            pdf_header_present = True
        hasher.update(data)

    file_hash = hasher.hexdigest()

    await file.seek(0)
    file.file.seek(0)

    storage.upload_fileobj(
        file.file,
        get_default_bucket(),
        file_hash,
        ExtraArgs={"ContentType": file.content_type},
    )

    return tasks.add_document_task(request, file_hash)


@v1_router.get("/{id}", response_model=Task)
def get_task(id: int, _: User = Depends(task_id_reachable)):
    return tasks.get_task(id)


@v1_router.get("/{id}/file")
def get_document_file(id: int, _: User = Depends(task_id_reachable)):
    file_hash = tasks.get_document_file_hash(id)
    file = storage.get_object(Bucket=get_default_bucket(), Key=file_hash)
    print(file, flush=True)
    return StreamingResponse(file["Body"].iter_chunks(), media_type="application_pdf")


@v1_router.delete("/{id}")
def delete_task(id, _: User = Depends(task_id_reachable)):
    tasks.delete_task(id)


@v1_router.patch("/{id}")
def update_task_by_id(
    id: int, request: TaskUpdate, _: User = Depends(task_id_reachable)
):
    if request.deadline:
        tasks.change_task_deadline(id, request.deadline)
    if request.title:
        tasks.change_task_title(id, request.title)

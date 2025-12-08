from fastapi import APIRouter, Depends, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from ..services import tasks

import fleep
from ..services.auth import logged_in, moderator, admin, owns_channel, \
                            task_id_reachable
from ..core.security import generate_uuid

from ..models.tasks import DocumentTaskCreationRequest, Task, \
                           TodoTaskCreationRequest, TaskDeadline, \
                           TaskTitle
from ..models.users import User
from typing import Annotated

import hashlib
import os
import datetime

v1_router = APIRouter(prefix="/tasks", tags=["tasks"])
os.makedirs("./uploads/", exist_ok=True)
os.makedirs("./tmp/", exist_ok=True)


@v1_router.get("/")
def get_tasks(user: User = Depends(logged_in)):
    return tasks.get_tasks(user.channel)


@v1_router.post("/todo")
def add_todo_task(request: TodoTaskCreationRequest,
                  owns_channel: str = Depends(owns_channel)):
    if owns_channel != "" and owns_channel != request.channel:
        raise HTTPException(403,
                            "Insufficient rights to manage external channels.")
    request.channel = owns_channel if owns_channel != "" \
        else request.channel

    tasks.add_todo_task(request)


@v1_router.post("/document")
async def add_document_task(file: UploadFile,
                            channel: Annotated[str, Form()],
                            title: Annotated[str, Form()],
                            subject: Annotated[str, Form()],
                            deadline: Annotated[datetime.datetime, Form()],
                            owns_channel: str = Depends(owns_channel)):

    if file.size > 20*1024*1024:
        raise HTTPException(413,
                            "File upload limit has been exceeded (20 MB).")

    request = DocumentTaskCreationRequest(
        subject=subject,
        title=title,
        channel=channel,
        deadline=deadline
    )

    if owns_channel != "" and owns_channel != channel:
        raise HTTPException(403,
                            "Insufficient rights to manage external channels.")
    request.channel = owns_channel if owns_channel != "" \
        else request.channel

    handle = generate_uuid()
    hasher = hashlib.md5()
    pdf_header_present = False

    with open(f"./tmp/{handle}", "wb") as f:
        while data := await file.read(2048):
            if not pdf_header_present:
                info = fleep.get(data)
                if not info.extension_matches("pdf"):
                    raise HTTPException(400,
                                        "No PDF header on upload.")
                pdf_header_present = True
            f.write(data)
            hasher.update(data)

    file_hash = hasher.hexdigest()
    os.rename(f"./tmp/{handle}", f"./uploads/{file_hash}")

    tasks.add_document_task(request, file_hash)


@v1_router.get("/{id}", response_model=Task)
def get_task(id: int,
             permitted: User = Depends(task_id_reachable)):
    return tasks.get_task(id)


@v1_router.get("/{id}/file")
def get_document_file(id: int,
                      permitted: User = Depends(task_id_reachable)):
    file_hash = tasks.get_document_file_hash(id)
    return FileResponse(f"./uploads/{file_hash}", media_type="application_pdf")


@v1_router.delete("/{id}")
def delete_task(id,
                permitted: User = Depends(task_id_reachable)):
    tasks.delete_task(id)


@v1_router.patch("/{id}/deadline")
def change_task_deadline(id: int,
                         request: TaskDeadline,
                         permitted: User = Depends(task_id_reachable)):
    tasks.change_task_deadline(id, request.deadline)


@v1_router.patch("/{id}/title")
def change_task_heading(id: int,
                        request: TaskTitle,
                        permitted: User = Depends(task_id_reachable)):
    tasks.change_task_heading(id, request.title)

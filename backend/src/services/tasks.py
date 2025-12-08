from ..database import db
from ..schemas.tasks import Task as TaskSchema, task_from_schema
from typing import List
from sqlalchemy.exc import NoResultFound
from ..models.tasks import Task as TaskModel, \
    TodoTaskCreationRequest, DocumentTaskCreationRequest

from sqlalchemy import select
from fastapi import HTTPException
from ..models.users import User as UserModel

import datetime

def add_todo_task(request: TodoTaskCreationRequest):
    with db.Session() as session:
        session.add(TaskSchema(channel=request.channel,
                               title=request.title,
                               deadline=request.deadline,
                               subtasks=request.subtasks,
                               subject=request.subject,
                               type="todo"))
        session.commit()


def add_document_task(request: DocumentTaskCreationRequest, file_hash: str):
    with db.Session() as session:
        session.add(TaskSchema(channel=request.channel, title=request.title,
                               deadline=request.deadline, fileHash=file_hash,
                               subject=request.subject, type="document"))
        session.commit()


def get_tasks(channel):
    tasks = None

    query = select(TaskSchema)
    if channel != "":
        query = query \
            .where(TaskSchema.channel == channel)
    with db.Session() as session:
        tasks = session.scalars(query).all()

    return tasks


def get_task(id: int) -> TaskModel:
    with db.Session() as session:
        task = session.get(TaskSchema, id)
        if not task:
            raise HTTPException(status_code=404,
                                detail=f"Task (id={id}) not found")
        return task_from_schema(task)


def delete_task(id: int):
    with db.Session() as session:
        task = session.get(TaskSchema, id)
        session.delete(task)
        session.commit()


def change_task_deadline(id, deadline: datetime.datetime):
    with db.Session() as session:
        task = session.get(TaskSchema, id)
        task.deadline = deadline
        task.modifiedAt = datetime.datetime.now()
        session.commit()


def change_task_title(id, title: str):
    with db.Session() as session:
        task = session.get(TaskSchema, id)
        task.title = title
        task.modifiedAt = datetime.datetime.now()
        session.commit()


def get_document_file_hash(id: int) -> str:
    task = get_task(id)
    if task.type != "document":
        raise HTTPException(400,
                            f"Task ID {id} is not of document type.")
    return task.fileHash

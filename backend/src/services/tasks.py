from ..database import db
from ..schemas.tasks import Task as TaskSchema, task_from_schema
from typing import List

from sqlalchemy.exc import NoResultFound
from ..models.tasks import Task as TaskModel, \
    TodoTaskCreationRequest, DocumentTaskCreationRequest

from sqlalchemy import select
from fastapi import HTTPException
from ..models.users import User as UserModel


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
    try:
        with db.Session() as session:
            task = session.get(TaskSchema, id)
        return task_from_schema(task)
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"Task (id={id}) not found")


def delete_task(id):
    pass


def change_task_deadline(id):
    pass


def change_task_heading(id):
    pass


def change_task_body(id):
    pass

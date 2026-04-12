import datetime

from fastapi import HTTPException
from sqlalchemy import select

from ..database import db
from ..models.tasks import Task as TaskModel
from ..schemas.tasks import DocumentTaskCreate, TodoTaskCreate
from ..schemas.tasks import Task as TaskSchema


def add_todo_task(request: TodoTaskCreate) -> int:
    with db.Session.begin() as session:
        newTask = TaskModel(
            channel=request.channel,
            title=request.title,
            deadline=request.deadline,
            subtasks=request.subtasks,
            subject=request.subject,
            type="todo",
        )
        session.add(newTask)

        return newTask.id


def add_document_task(request: DocumentTaskCreate, file_hash: str) -> int:
    with db.Session.begin() as session:
        newTask = TaskModel(
            channel=request.channel,
            title=request.title,
            deadline=request.deadline,
            fileHash=file_hash,
            subject=request.subject,
            type="document",
        )
        session.add(newTask)

        return newTask.id


def get_tasks(channel) -> list[TaskSchema]:
    tasks: list[TaskSchema] = []

    query = select(TaskModel)
    if channel != "":
        query = query.where(TaskModel.channel == channel)

    with db.Session() as session:
        tasks = [TaskSchema.model_validate(x) for x in session.scalars(query).all()]

    return tasks


def get_task(id: int) -> TaskSchema:
    with db.Session() as session:
        task = session.get(TaskModel, id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task (id={id}) not found")
        return TaskSchema.model_validate(task)


def delete_task(id: int):
    with db.Session.begin() as session:
        task = session.get(TaskModel, id)
        session.delete(task)


def change_task_deadline(id, deadline: datetime.datetime):
    with db.Session() as session:
        task = session.get(TaskModel, id)
        if task:
            task.deadline = deadline
            task.modifiedAt = datetime.datetime.now()
        session.commit()


def change_task_title(id, title: str):
    with db.Session() as session:
        task = session.get(TaskModel, id)
        if task:
            task.title = title
            task.modifiedAt = datetime.datetime.now()
        session.commit()


def get_document_file_hash(id: int) -> str | None:
    task = get_task(id)
    if task.type != "document":
        raise HTTPException(400, f"Task ID {id} is not of document type.")
    return task.fileHash

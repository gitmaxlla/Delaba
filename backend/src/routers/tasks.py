from fastapi import APIRouter, Depends
from ..services import tasks

from ..services.auth import require_user, require_edit
from ..services.users import User


v1_router = APIRouter(prefix="/tasks", tags=["tasks"])


@v1_router.get("/")
def get_all_tasks(user: User = Depends(require_user)):
    tasks.get_all_tasks()


@v1_router.put("/")
def add_task(authorized: bool = Depends(require_edit)):
    return authorized
    tasks.add_task()


@v1_router.get("/{id}")
def get_task(id):
    tasks.get_task(id)


@v1_router.delete("/{id}")
def delete_task(id):
    tasks.delete_task(id)


@v1_router.patch("/{id}/deadline")
def change_task_deadline(id):
    tasks.change_task_deadline(id)


@v1_router.patch("/{id}/heading")
def change_task_heading(id):
    tasks.change_task_heading(id)


@v1_router.patch("/{id}/body")
def change_task_body(id):
    tasks.change_task_body(id)

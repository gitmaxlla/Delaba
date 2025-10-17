from fastapi import APIRouter
from ..services import tasks_service


v1_router = APIRouter(prefix="/tasks", tags=["tasks"])


@v1_router.get("/")
def get_all_tasks():
    tasks_service.get_all_tasks()


@v1_router.put("/")
def add_task():
    tasks_service.add_task()


@v1_router.get("/{id}")
def get_task(id):
    tasks_service.get_task(id)


@v1_router.delete("/{id}")
def delete_task(id):
    tasks_service.delete_task(id)


@v1_router.patch("/{id}/deadline")
def change_task_deadline(id):
    tasks_service.change_task_deadline(id)


@v1_router.patch("/{id}/heading")
def change_task_heading(id):
    tasks_service.change_task_heading(id)


@v1_router.patch("/{id}/body")
def change_task_body(id):
    tasks_service.change_task_body(id)

from fastapi import APIRouter, Depends
from ..services import users_service


v1_router = APIRouter(prefix="/users", tags=["users"])


@v1_router.get("/")
def get_all_users():
    users_service.get_all_users()


@v1_router.delete("/")
def delete_all_users():
    users_service.delete_all_users()


@v1_router.put("/")
def add_an_user():
    users_service.add_an_user()


@v1_router.get("/{id}")
def get_user(id):
    users_service.get_user(id)


@v1_router.delete("/{id}")
def delete_user(id):
    users_service.delete_user(id)


@v1_router.get("/{id}")
def get_user_data(id):
    users_service.get_user_data(id)


@v1_router.put("/{id}")
def update_user_data(id):
    users_service.update_user_data(id)

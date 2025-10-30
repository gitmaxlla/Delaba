from fastapi import APIRouter, Depends
from ..services import users


v1_router = APIRouter(prefix="/users", tags=["users"])


@v1_router.get("/")
def get_all_users():
    users.get_all_users()


@v1_router.delete("/")
def delete_all_users():
    users.delete_all_users()


@v1_router.put("/")
def add_an_user():
    users.add_an_user()


@v1_router.get("/{id}")
def get_user(id):
    users.get_user(id)


@v1_router.delete("/{id}")
def delete_user(id):
    users.delete_user(id)


@v1_router.get("/{id}")
def get_user_data(id):
    users.get_user_data(id)


@v1_router.put("/{id}")
def update_user_data(id):
    users.update_user_data(id)

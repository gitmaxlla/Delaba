from fastapi import APIRouter, HTTPException, Depends
from ..services import users
from typing import List

from ..models.users import Permissions, User as UserModel
from ..schemas.users import user_from_schema
from ..services.auth import require_admin

v1_router = APIRouter(prefix="/users", tags=["users"])


@v1_router.get("/", response_model=List[UserModel])
def get_all_users(is_admin: bool = Depends(require_admin)):
    if not is_admin:
        raise HTTPException(403)
    return users.get_all_users()


@v1_router.delete("/", response_model=None)
def delete_all_users():
    users.delete_all_users()


@v1_router.post("/")
def add_an_user(
        name: str,
        channel: str,
        is_admin: bool = Depends(require_admin)):
    if not is_admin:
        raise HTTPException(403)
    return users.add_an_user(name=name, channel=channel)


@v1_router.get("/{id}", response_model=UserModel)
def get_user(id):
    res = users.get_user(id)
    if not res:
        raise HTTPException(status_code=404, detail=f"User (id={id}) not found")
    return res


@v1_router.delete("/{id}", response_model=None)
def delete_user(id):
    users.delete_user(id)


@v1_router.put("/{id}")
def update_user_data(id, data: dict):
    users.update_user_data(id, data)

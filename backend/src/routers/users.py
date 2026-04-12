from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.channels import ChannelCreate
from src.schemas.users import (
    AdminCreate,
    PermissionTags,
    User,
    UserCreate,
)
from src.schemas.users import (
    User as UserModel,
)
from src.services import users
from src.services.auth import admin, logged_in, manages_user_id, moderator, owns_channel


v1_router = APIRouter(prefix="/users", tags=["users"])


@v1_router.get("/data", response_model=dict)
def get_user_data(user: User = Depends(logged_in)):
    return users.get_user_data(user.id)


@v1_router.get("/permissions", response_model=int)
def get_self_permissions(user: User = Depends(logged_in)):
    return users.get_user_permissions(user.id)


@v1_router.get("/", response_model=List[UserModel])
def get_users(
    page: Annotated[int, Query(ge=0)] = 0,
    page_size: Annotated[int, Query(ge=1, le=50)] = 50,
    moderator: UserModel = Depends(moderator),
):
    return users.get_by_channel(moderator.channel, page, page_size)


@v1_router.get("/{id}", response_model=UserModel)
def get_user(id):
    return users.get_user(id)


@v1_router.get("/{id}/data", response_model=dict)
def get_user_data_by_id(id, _: User = Depends(admin)):
    return users.get_user_data(id)


@v1_router.put("/data")
def update_user_data(data: dict, user: User = Depends(logged_in)):
    users.update_user_data(user.id, data)


@v1_router.post("/moderator")
def add_moderator(request: UserCreate, _: UserModel = Depends(admin)):
    return users.add_user(
        login=request.login,
        role=request.role,
        channel=request.channel,
        permissions=(PermissionTags.MANAGE_CHANNEL & PermissionTags.VIEW_CHANNEL),
    )


@v1_router.post("/admin")
def add_admin(request: AdminCreate, _: UserModel = Depends(admin)):
    return users.add_user(
        login=request.login,
        role=request.role,
        channel="",
        permissions=(
            PermissionTags.MANAGE_CHANNEL
            & PermissionTags.VIEW_CHANNEL
            & PermissionTags.ADMIN
        ),
    )


@v1_router.post("/")
def add_user(request: UserCreate, owns_channel: str = Depends(owns_channel)):

    # TODO: Replace with admin rights check for user
    if owns_channel != "" and owns_channel != request.channel:
        raise HTTPException(403, "Insufficient rights to manage external channels.")
    request.channel = owns_channel if owns_channel != "" else request.channel

    users.add_user(
        login=request.login,
        role=request.role,
        channel=request.channel,
        permissions=PermissionTags.VIEW_CHANNEL,
    )


@v1_router.delete("/{id}", response_model=None)
def delete_user(id, _: User = Depends(manages_user_id)):
    users.delete_user(id)


@v1_router.patch("/{id}/channel")
async def transfer_user(id: int, request: ChannelCreate, _: User = Depends(admin)):
    await users.transfer_user(id, request.channel)


@v1_router.get("/{id}/ban")
async def ban_user(user: User = Depends(manages_user_id)):
    await users.ban_user(user.id)


@v1_router.get("/{id}/unban")
async def unban_user(user: User = Depends(manages_user_id)):
    await users.unban_user(user.id)

from fastapi import APIRouter, Depends, HTTPException
from ..services import users
from typing import List

from ..models.users import User as UserModel, \
    UserCreationRequest, UserCreationResponse, User, \
    Permissions, AdminCreationRequest
from ..services.auth import admin, logged_in, moderator, \
                            owns_channel, manages_user_id
from ..models.channels import ChannelRequest

v1_router = APIRouter(prefix="/users", tags=["users"])


@v1_router.get("/data", response_model=dict)
def get_user_data(user: User = Depends(logged_in)):
    return users.get_user_data(user)


@v1_router.get("/permissions", response_model=int)
def get_self_permissions(user: User = Depends(logged_in)):
    return users.get_user_permissions(user)


@v1_router.get("/", response_model=List[UserModel])
def get_users(moderator: UserModel = Depends(moderator)):
    return users.get_by_channel(moderator.channel)


@v1_router.get("/{id}", response_model=UserModel)
def get_user(id):
    return users.get_user(id)


@v1_router.get("/{id}/data", response_model=dict)
def get_user_data_by_id(id, admin: User = Depends(admin)):
    return users.get_user_data(users.get_user(id))


@v1_router.put("/data")
def update_user_data(data: dict, user: User = Depends(logged_in)):
    users.update_user_data(user, data)


@v1_router.post("/moderator")
def add_moderator(request: UserCreationRequest,
                  admin: UserModel = Depends(admin)) -> UserCreationResponse:
    return users.add_user(login=request.login,
                          role=request.role,
                          channel=request.channel,
                          permissions=(Permissions.MANAGE_CHANNEL
                                       & Permissions.VIEW_CHANNEL))


@v1_router.post("/admin")
def add_admin(request: AdminCreationRequest,
              admin: UserModel = Depends(admin)) -> UserCreationResponse:
    return users.add_user(login=request.login,
                          role=request.role,
                          channel="",
                          permissions=(Permissions.MANAGE_CHANNEL
                                       & Permissions.VIEW_CHANNEL
                                       & Permissions.ADMIN))


@v1_router.post("/")
def add_user(request: UserCreationRequest,
             owns_channel: str = Depends(owns_channel)) \
             -> UserCreationResponse:

    if owns_channel != "" and owns_channel != request.channel:
        raise HTTPException(403,
                            "Insufficient rights to manage external channels.")
    request.channel = owns_channel if owns_channel != "" \
        else request.channel

    return users.add_user(login=request.login,
                          role=request.role,
                          channel=request.channel,
                          permissions=Permissions.VIEW_CHANNEL)


@v1_router.delete("/{id}", response_model=None)
def delete_user(id, user: User = Depends(manages_user_id)):
    users.delete_user(id)


@v1_router.patch("/{id}/channel")
def transfer_user(id: int, request: ChannelRequest,
                  user: User = Depends(admin)):
    users.transfer_user(user.id, request.channel)


@v1_router.get("/{id}/ban")
def ban_user(user: User = Depends(manages_user_id)):
    users.ban_user(user.id)


@v1_router.get("/{id}/unban")
def unban_user(user: User = Depends(manages_user_id)):
    users.unban_user(user.id)

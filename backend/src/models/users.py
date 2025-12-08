from pydantic import BaseModel
from enum import IntFlag


class Permissions(IntFlag):
    BANNED = 1
    VIEW_CHANNEL = 2
    MANAGE_CHANNEL = 4
    ADMIN = 8


class User(BaseModel):
    id: int
    login: str
    initialized: bool

    role: str
    channel: str
    permissions: Permissions


class UserCreationRequest(BaseModel):
    login: str
    role: str
    channel: str


class AdminCreationRequest(BaseModel):
    login: str
    role: str


class UserCreationResponse(BaseModel):
    id: int
    init_token: str


class Credentials(BaseModel):
    login: str
    password: str


class InitCredentials(BaseModel):
    login: str
    init_token: str
    new_password: str


def has_moderator_rights(user: User) -> bool:
    return ((user.permissions & Permissions.MANAGE_CHANNEL)
            == Permissions.MANAGE_CHANNEL)


def has_admin_rights(user: User) -> bool:
    return ((user.permissions & Permissions.ADMIN)
            == Permissions.ADMIN)


def banned(user: User) -> bool:
    return ((user.permissions & Permissions.BANNED)
            == Permissions.BANNED)

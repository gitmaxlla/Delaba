from pydantic import BaseModel
from enum import IntFlag


class Permissions(IntFlag):
    BANNED = 0
    VIEW_CHANNEL = 1
    MANAGE_CHANNEL = 2
    ADMIN = 8


class User(BaseModel):
    id: int
    name: str

    initialized: bool
    password_hashed: str

    channel: str
    permissions: Permissions

    data: dict

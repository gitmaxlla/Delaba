from pydantic import BaseModel, ConfigDict
from ..core.permissions import Permissions


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    initialized: bool

    role: str
    channel: str
    permissions: Permissions


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    role: str
    channel: str


class AdminCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    role: str


class Credentials(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    password: str


class InitCredentials(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    init_password: str
    new_password: str

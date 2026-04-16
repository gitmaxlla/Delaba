from pydantic import BaseModel, ConfigDict
from ..core.permissions import PermissionTags


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    initialized: bool

    role: str
    channel: str
    permissions: PermissionTags


class UsersPaginatedResponse(BaseModel):
    values: list[User]
    total: int


class UserCreate(BaseModel):
    login: str
    role: str
    channel: str


class AdminCreate(BaseModel):
    login: str
    role: str


class Credentials(BaseModel):
    login: str
    password: str


class InitCredentials(BaseModel):
    login: str
    init_password: str
    new_password: str

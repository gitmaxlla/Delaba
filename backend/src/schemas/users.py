from ..database.db import Base
from sqlalchemy.dialects.postgresql import BIT, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from ..models.users import Permissions, User as UserModel
from ..core.security import generate_uuid
import math


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="", unique=True)

    password_hashed: Mapped[str] = mapped_column(String())
    initialized: Mapped[Boolean] = mapped_column(Boolean(), default=False)

    channel: Mapped[str] = mapped_column(default=generate_uuid())

    permissions: Mapped[Permissions] = \
        mapped_column(
            BIT(1 + math.floor(math.log(1 + max(Permissions), 2)), False))

    data: Mapped[JSONB] = mapped_column(JSONB, default={})


def user_from_schema(user: User) -> User:
    user = user.__dict__
    user["permissions"] = int(user["permissions"], 2)
    return UserModel.model_validate(user)

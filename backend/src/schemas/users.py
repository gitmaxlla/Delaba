from ..database.db import Base
from sqlalchemy.dialects.postgresql import BIT, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey
from ..models.users import Permissions, User as UserModel
import math


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(default="Студент")

    channel: Mapped[str] = \
        mapped_column(ForeignKey("channels.name", ondelete="CASCADE"))

    permissions: Mapped[Permissions] = \
        mapped_column(
            BIT(1 + math.floor(math.log(1 + max(Permissions), 2)), False))

    login: Mapped[str] = mapped_column(unique=True)
    password_hashed: Mapped[str] = mapped_column(String())
    initialized: Mapped[Boolean] = mapped_column(Boolean(), default=False)

    data: Mapped[JSONB] = mapped_column(JSONB, default={})


def user_from_schema(user: User) -> UserModel:
    user = user.__dict__
    user["permissions"] = int(user["permissions"], 2)
    return UserModel.model_validate(user)

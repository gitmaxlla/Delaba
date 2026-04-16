from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.config import DEFAULT_ROLE
from src.core.permissions import PermissionTags, Permissions
from src.models.base import Base
from src.schemas.news import News


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(default=DEFAULT_ROLE)

    channel: Mapped[str] = mapped_column(ForeignKey("channels.name"))

    permissions: Mapped[PermissionTags] = mapped_column(Permissions())

    login: Mapped[str] = mapped_column(unique=True)
    password_hashed: Mapped[str] = mapped_column(String())
    initialized: Mapped[bool] = mapped_column(default=False)

    data: Mapped[dict[str, Any]] = mapped_column(JSONB, default={})

    news: Mapped["News"] = relationship(backref="user", cascade="all, delete")

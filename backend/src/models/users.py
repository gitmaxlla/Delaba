import math
from typing import Any

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import BIT, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.config import DEFAULT_ROLE
from src.core.permissions import Permissions
from src.database.db import Base
from src.schemas.news import News


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(default=DEFAULT_ROLE)

    channel: Mapped[str] = mapped_column(ForeignKey("channels.name"))

    # TODO: Manage all permissions with TypeDeclaration instead of this mess
    permissions: Mapped[str] = mapped_column(
        BIT(1 + math.floor(math.log(1 + max(Permissions), 2)), False)
    )

    login: Mapped[str] = mapped_column(unique=True)
    password_hashed: Mapped[str] = mapped_column(String())
    initialized: Mapped[Boolean] = mapped_column(Boolean(), default=False)

    data: Mapped[dict[str, Any]] = mapped_column(JSONB, default={})

    news: Mapped["News"] = relationship(backref="user", cascade="all, delete")

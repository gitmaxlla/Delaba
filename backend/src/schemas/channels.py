from ..database.db import Base
from sqlalchemy.orm import Mapped, mapped_column


class Channel(Base):
    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(primary_key=True)

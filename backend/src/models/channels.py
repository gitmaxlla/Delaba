from ..database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..schemas.news import News
from ..schemas.tasks import Task
from ..schemas.users import User


class Channel(Base):
    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(primary_key=True)

    news: Mapped["News"] = relationship(backref="channel_news",
                                        cascade="all, delete")
    task: Mapped["Task"] = relationship(backref="channel_task",
                                        cascade="all, delete")
    user: Mapped["User"] = relationship(backref="channel_user",
                                        cascade="all, delete")

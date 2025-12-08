from ..database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, ForeignKey

import datetime
from ..models.news import News as NewsModel


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    section: Mapped[str] = mapped_column(nullable=True)

    postedAt: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now())

    by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    message: Mapped[str] = mapped_column()


def news_from_schema(news: News) -> NewsModel:
    news = news.__dict__
    return NewsModel.model_validate(news)

from ..database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, String, ForeignKey

from ..models.documents import Document as DocumentModel, \
    DocumentEvent as DocumentEventModel
import datetime


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    createdAt: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now)

    subject: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    deadline: Mapped[datetime.datetime] = mapped_column(DateTime)

    fileHash: Mapped[str] = mapped_column()


class DocumentEvent(Base):
    __tablename__ = "document_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    postedAt: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now)
    by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message: Mapped[str] = mapped_column()


def document_from_schema(document: Document) -> DocumentModel:
    document = document.__dict__
    return DocumentModel.model_validate(document)


def document_event_from_schema(
        documentEvent: DocumentEvent) -> DocumentEventModel:
    documentEvent = documentEvent.__dict__
    return DocumentEventModel.model_validate(documentEvent)

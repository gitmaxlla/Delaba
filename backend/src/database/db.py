from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy_utils import database_exists, create_database

from ..core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(engine, autocommit=False)


class Base(DeclarativeBase):
    pass


def drop_all():
    Base.metadata.drop_all(engine)


def create_all():
    Base.metadata.create_all(engine)

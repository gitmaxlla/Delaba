from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from src.core.config import DATABASE_URL, SQLALCHEMY_ECHO


engine = create_engine(DATABASE_URL, echo=SQLALCHEMY_ECHO)
if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(engine, autocommit=False)


class Base(DeclarativeBase):
    pass


def create_all():
    Base.metadata.create_all(engine)


def drop_all():
    Base.metadata.drop_all(engine)

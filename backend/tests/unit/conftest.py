import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from src.models.base import Base
from src.models.channels import Channel
from src.models.news import News
from src.models.tasks import Task
from src.models.users import User


INCLUDE_SCHEMAS = Channel, News, Task, User


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def get_test_db(engine):
    conn = engine.connect()
    transaction = conn.begin()
    session = sessionmaker(bind=conn)()

    yield session

    session.close()
    transaction.rollback()
    conn.close()


@pytest.fixture
def get_test_users(get_test_db, get_test_data):
    get_test_db.merge(get_test_data["ch1"])
    get_test_db.merge(get_test_data["ch2"])
    admin = get_test_data["a"]
    admin = get_test_db.merge(admin)
    user = get_test_data["u"]
    user = get_test_db.merge(user)
    get_test_db.flush()

    return {"admin": admin, "user": user}

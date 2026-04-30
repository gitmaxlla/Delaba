import pytest
from src.core.config import DATABASE_URL
from src.core.permissions import PermissionTags
from src.database import obj
from src.database.db import get_db
from src.models.users import User
from src.services.auth import require_access
from alembic.config import Config
from alembic import command
from fastapi.testclient import TestClient
from src.services.users import get_user
from src.main import app


@pytest.fixture(scope="session")
def run_migrations():
    obj.create_default_bucket()
    migration_cfg = Config("alembic.ini")
    migration_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.upgrade(migration_cfg, "head")


@pytest.fixture(scope="session")
def get_real_db():
    gen = get_db()
    session = next(gen)
    try:
        yield session
    finally:
        try:
            next(gen)
        except StopIteration:
            pass


@pytest.fixture(scope="session")
def get_test_users(get_real_db, get_test_data):
    # Not graceful yikes
    try:
        get_real_db.merge(get_test_data["ch1"])
        get_real_db.merge(get_test_data["ch2"])
        get_real_db.merge(get_test_data["a"])
        get_real_db.merge(get_test_data["u"])
        get_real_db.commit()
    except Exception:
        pass


@pytest.fixture(scope="session")
def client(run_migrations, get_test_users):
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_admin_auth():
    app.dependency_overrides[require_access] = lambda: User(
        id=1,
        login="admin_login",
        role="admin",
        permissions=PermissionTags.ADMIN,
        password_hashed="admin_password",
        channel="",
    )

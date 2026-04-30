import pytest

from src.core.permissions import PermissionTags
from src.models.channels import Channel
from src.models.users import User

from src.core.security import hash as pwdlib_hash


@pytest.fixture(scope="session")
def get_test_data():
    return {
        "ch1": Channel(name=""),
        "ch2": Channel(name="test"),
        "a": User(
            login="admin_login",
            role="admin",
            permissions=PermissionTags.ADMIN,
            password_hashed=pwdlib_hash("admin_password"),
            channel="",
        ),
        "u": User(
            login="user_login",
            role="user",
            permissions=PermissionTags.VIEW_CHANNEL,
            password_hashed=pwdlib_hash("user_password"),
            channel="test",
        ),
    }

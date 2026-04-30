import pytest
from src.routers.channels import get_channels


@pytest.mark.parametrize("get_test_users", ["get_test_db"], indirect=True)
def test_admin_sees_all_channels(get_test_db, get_test_users):
    assert len(get_channels(get_test_users["admin"], get_test_db)) == 2
    assert len(get_channels(get_test_users["user"], get_test_db)) == 1

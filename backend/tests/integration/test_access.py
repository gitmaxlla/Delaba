import datetime
import pytest
import time_machine
from datetime import timedelta
from src.core.config import REFRESH_TOKEN_EXPIRES_TIME_SEC


def test_uninitialized_user_login_attempt(client, mock_admin_auth):
    response = client.post(
        "/v1/auth/login", json={"login": "admin_login", "password": "admin_password"}
    )

    assert response.status_code == 403


def test_refresh_expiry(client, mock_admin_auth):
    response = client.post(
        "/v1/auth/init",
        json={
            "login": "admin_login",
            "init_password": "admin_password",
            "new_password": "admin_password",
        },
    )

    assert response.status_code == 200

    response = client.post("/v1/auth/refresh")
    assert response.status_code == 200

    with time_machine.travel(
        datetime.datetime.now() + timedelta(seconds=1 + REFRESH_TOKEN_EXPIRES_TIME_SEC)
    ):
        response = client.post("/v1/auth/refresh")
        assert response.status_code == 401

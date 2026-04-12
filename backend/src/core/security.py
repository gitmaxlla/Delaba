import datetime
import secrets
import string
import uuid
from collections import defaultdict
from time import time

import jwt
from pwdlib import PasswordHash

from .base import Singleton
from .config import (
    ACCESS_SIGNATURE,
    ACCESS_TOKEN_EXPIRES_TIME_SEC,
    REFRESH_SIGNATURE,
    REFRESH_TOKEN_EXPIRES_TIME_SEC,
    REQUESTS_PER_MINUTE_LIMIT,
)


# TODO: what's this class doing at all?
class TokenPayload:
    __slots__ = "id"

    def __init__(self, id):
        self.id = id


def hash(value: str) -> str:
    return PasswordHash.recommended().hash(value)


def validate_hash(value: str, hash: str) -> bool:
    return PasswordHash.recommended().verify(value, hash)


def generate_password(length=16) -> str:
    charset = string.ascii_letters + string.digits
    return "".join([secrets.choice(charset) for i in range(length)])


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_access_token(id: int) -> str:
    access_payload = {
        "id": id,
        "exp": int(time()) + ACCESS_TOKEN_EXPIRES_TIME_SEC,
        "type": "access",
    }

    access_token = jwt.encode(access_payload, ACCESS_SIGNATURE, algorithm="HS256")

    return access_token


def generate_refresh_token(id: int) -> str:
    refresh_payload = {
        "id": id,
        "exp": int(time()) + REFRESH_TOKEN_EXPIRES_TIME_SEC,
        "type": "refresh",
    }
    refresh_token = jwt.encode(refresh_payload, REFRESH_SIGNATURE, algorithm="HS256")

    return refresh_token


def get_access_payload(token: str) -> dict:
    return dict(jwt.decode(token, ACCESS_SIGNATURE, algorithms="HS256"))


def get_refresh_payload(token: str) -> dict:
    return dict(jwt.decode(token, REFRESH_SIGNATURE, algorithms="HS256"))


class RateLimiter(metaclass=Singleton):
    def __init__(self, per_minute=REQUESTS_PER_MINUTE_LIMIT):
        self.requests_counter = defaultdict(int)
        self.requests_started = defaultdict(datetime.datetime.now)
        self.per_minute = per_minute

    def exceeded(self, client_id) -> float:
        time_delta = datetime.datetime.now() - self.requests_started[client_id]
        self.requests_counter[client_id] += 1

        if time_delta.total_seconds() >= 60:
            self.requests_started[client_id] = datetime.datetime.now()
            self.requests_counter[client_id] = 0
        elif self.requests_counter[client_id] > self.per_minute:
            return 60 - time_delta.total_seconds()

        return 0

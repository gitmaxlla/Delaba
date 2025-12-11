from pwdlib import PasswordHash
import jwt
import uuid
import datetime
from time import time
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv("../.env")

DAY_SECS = 60 * 60 * 24
REFRESH_TOKEN_EXPIRES_TIME_SEC = DAY_SECS * 20
ACCESS_TOKEN_EXPIRES_TIME_SEC = 60

REFRESH_SIGNATURE = os.getenv("JWT_REFRESH_SECRET")
ACCESS_SIGNATURE = os.getenv("JWT_ACCESS_SECRET")


def hash(value: str):
    return PasswordHash.recommended().hash(value)


def validate_hash(value: str, hash: str) -> bool:
    return PasswordHash.recommended().verify(value, hash)


def generate_uuid():
    return str(uuid.uuid4())


def generate_access_token(id: int) -> str:
    access_payload = {
        "id": id,
        "exp": int(time()) + ACCESS_TOKEN_EXPIRES_TIME_SEC,
        "type": "access"
    }

    access_token = jwt.encode(access_payload,
                              ACCESS_SIGNATURE, algorithm="HS256")

    return access_token


def generate_refresh_token(id: int) -> str:
    refresh_payload = {
        "id": id,
        "exp": int(time()) + REFRESH_TOKEN_EXPIRES_TIME_SEC,
        "type": "refresh"
    }
    refresh_token = jwt.encode(refresh_payload,
                               REFRESH_SIGNATURE, algorithm="HS256")

    return refresh_token


def get_access_payload(token: str) -> dict:
    return dict(jwt.decode(token, ACCESS_SIGNATURE, algorithms="HS256"))


def get_refresh_payload(token: str) -> dict:
    return dict(jwt.decode(token, REFRESH_SIGNATURE, algorithms="HS256"))


class RateLimiter:
    def __init__(self, per_minute=300):
        self.requests_counter = defaultdict(int)
        self.requests_started = defaultdict(datetime.datetime.now)
        self.per_minute = per_minute

    def exceeded(self, clientID):
        time_delta = \
            datetime.datetime.now() - self.requests_started[clientID]
        self.requests_counter[clientID] += 1

        if time_delta.total_seconds() >= 60:
            self.requests_started[clientID] = datetime.datetime.now()
            self.requests_counter[clientID] = 0
        elif self.requests_counter[clientID] > self.per_minute:
            return 60 - time_delta.total_seconds()

        return 0

import uuid
from pwdlib import PasswordHash

from collections import defaultdict
import datetime


def generate_uuid():
    return str(uuid.uuid4())


def hash(value: str):
    return PasswordHash.recommended().hash(value)


def validate(value: str, hash: str) -> bool:
    return PasswordHash.recommended().verify(value, hash)


class RateLimiter:
    def __init__(self, per_minute=20):
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

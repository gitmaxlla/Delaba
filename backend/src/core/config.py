import logging
import os
from typing import cast

DEFAULT_ROLE = "Студент"

# Using environ will generate exceptions on null conveniently
DATABASE_NAME = os.environ["POSTGRES_DB"]
DATABASE_USER = os.environ["POSTGRES_USER"]
DATABASE_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DATABASE_ADDRESS = os.environ["POSTGRES_ADDRESS"]
DATABASE_PORT = os.environ["POSTGRES_PORT"]

OBJ_STORAGE_DEFAULT_BUCKET = os.environ["MINIO_DEFAULT_BUCKET"]
OBJ_STORAGE_ROOT_USER = os.environ["MINIO_ROOT_USER"]
OBJ_STORAGE_ROOT_PASSWORD = os.environ["MINIO_ROOT_PASSWORD"]
OBJ_STORAGE_HOSTNAME = os.environ["MINIO_HOSTNAME"]
OBJ_STORAGE_PORT = os.environ["MINIO_PORT"]

ALLOWED_HOSTNAME = os.environ["SERVER_HOSTNAME"]
ADMIN_MAIL = os.environ["ADMIN_MAIL"]
DELABA_MAIL = os.environ["DELABA_MAIL"]

SMTP_HOSTNAME = os.environ["SMTP_HOSTNAME"]
SMTP_PORT = os.environ["SMTP_PORT"]

_db_location = f"{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"
_db_user = f"{DATABASE_USER}:{DATABASE_PASSWORD}"
DATABASE_URL = f"postgresql+psycopg://{_db_user}@{_db_location}"
SQLALCHEMY_ECHO = os.environ["SQLALCHEMY_ECHO"] == "true"
DEV_MODE = os.getenv("DEV_MODE") == "true"

OPENAI_ENDPOINT = os.environ["OPENAI_ENDPOINT"]
OPENAI_MODEL_TAG = os.environ["OPENAI_MODEL_TAG"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

DAY_SECS = 60 * 60 * 24
REFRESH_TOKEN_EXPIRES_TIME_SEC = DAY_SECS * 20
ACCESS_TOKEN_EXPIRES_TIME_SEC = 60
REFRESH_SIGNATURE = os.environ["JWT_REFRESH_SECRET"]
ACCESS_SIGNATURE = os.environ["JWT_ACCESS_SECRET"]

BYTES_PER_MB = 1024 * 1024
FILE_UPLOAD_LIMIT_BYTES = 20 * BYTES_PER_MB

REQUESTS_PER_MINUTE_LIMIT = 300


class LogFilter(logging.Filter):
    def filter(self, record):
        ACCESS_LOG_EXCLUDE = ["/"]

        if not isinstance(record.args, tuple) or not all(
            isinstance(x, str | int) for x in record.args
        ):
            return True

        args = cast(list[str], record.args)
        if args and len(args) >= 3:
            endpoint = args[2]
            if endpoint in ACCESS_LOG_EXCLUDE:
                return False

        return True

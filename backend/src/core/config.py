import os
import logging

DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_USER = os.getenv("POSTGRES_USER")

DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_ADDRESS = os.getenv("POSTGRES_ADDRESS")
DATABASE_PORT = os.getenv("POSTGRES_PORT")

_db_location = f"{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"
_db_user = f"{DATABASE_USER}:{DATABASE_PASSWORD}"

DATABASE_URL = f"postgresql+psycopg://{_db_user}@{_db_location}"
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO") == "true"

DEV_MODE = os.getenv("DEV_MODE") == "1"
ALLOWED_HOSTNAME = os.getenv("ALLOWED_HOSTNAME")

REFRESH_SIGNATURE = os.getenv("JWT_REFRESH_SECRET")
ACCESS_SIGNATURE = os.getenv("JWT_ACCESS_SECRET")

ADMIN_MAIL = os.getenv("ADMIN_MAIL")
DELABA_MAIL = os.getenv("DELABA_MAIL")

SMTP_HOSTNAME = os.getenv("SMTP_HOSTNAME")
SMTP_PORT = os.getenv("SMTP_PORT")


class LogFilter(logging.Filter):
    def filter(self, record):
        ACCESS_LOG_EXCLUDE = ["/"]
        if record.args and len(record.args) >= 3:
            if record.args[2] in ACCESS_LOG_EXCLUDE:
                return False
        return True

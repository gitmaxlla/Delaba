import os
from dotenv import load_dotenv

load_dotenv("../.env")

DATABASE_NAME = os.getenv("POSTGRES_DB")
DATABASE_USER = os.getenv("POSTGRES_USER")

DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_ADDRESS = os.getenv("POSTGRES_ADDRESS")
DATABASE_PORT = os.getenv("POSTGRES_PORT")

db_location = f"{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}"
db_user = f"{DATABASE_USER}:{DATABASE_PASSWORD}"
DATABASE_URL = f"postgresql+psycopg2://{db_user}@{db_location}"

SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO") == "true"

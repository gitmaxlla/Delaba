from dotenv import load_dotenv
import os

load_dotenv("../.env")
ADMIN_INIT_TOKEN = os.getenv("ADMIN_INIT_TOKEN")

import uvicorn
from src.core.config import DEV_MODE, DATABASE_URL
from src.database import obj

from alembic.config import Config
from alembic import command


if __name__ == "__main__":
    obj.create_default_bucket()
    migration_cfg = Config("alembic.ini")
    migration_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.upgrade(migration_cfg, "head")
    print("APP: Migrations applied", flush=True)

    uvicorn.run("src.main:app", host="0.0.0.0", reload=DEV_MODE)

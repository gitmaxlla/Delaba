import uvicorn
from src.core.config import DEV_MODE


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", reload=DEV_MODE)

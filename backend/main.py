from fastapi import FastAPI
from .routers import router, get_version_list

app = FastAPI()
app.include_router(router)


@app.get("/", tags=["app"])
async def about():
    """
    Check API availability and supported versions
    """

    return {"message": "Welcome to Delaba project API!",
            "versions": get_version_list()}

from fastapi import APIRouter, Depends
from typing import List

from src.schemas.users import User
from src.schemas.channels import ChannelCreate

from src.services.auth import admin, logged_in
from src.services.channels import (
    get_channels as get_channels_service,
    create_channel as create_channel_service,
    delete_channel as delete_channel_service,
)


v1_router = APIRouter(prefix="/channels", tags=["channels"])


@v1_router.get("/")
def get_channels(user: User = Depends(logged_in)) -> List[str]:
    return get_channels_service(user)


@v1_router.post("/")
def create_channel(channel: ChannelCreate, _: User = Depends(admin)):
    return create_channel_service(channel)


@v1_router.delete("/")
def delete_channel(channel: ChannelCreate, _: User = Depends(admin)):
    # raise HTTPException(403, "Removing root channel is not allowed.")
    delete_channel_service(channel)
    return delete_channel_service(channel)

from fastapi import APIRouter, Response
from ..services.users import ban_user, make_moderator, unban_user, \
                             make_admin, make_default
from ..services.auth import set_tokens

from ..services.users import add_user, Permissions
from ..services.channels import create_channel
from ..services.auth import TokenPayload

from ..models.channels import ChannelRequest

v1_router = APIRouter(prefix="/mock", tags=["mock"])


def mock_data():
    first_user_channel = create_channel(ChannelRequest(channel="123"))
    first_user_channel = create_channel(ChannelRequest(channel="456"))

    first_user_data = add_user("123", "123", "123", Permissions.VIEW_CHANNEL)

    user_data1 = add_user("one", "1", "123", Permissions.VIEW_CHANNEL)
    user_data2 = add_user("two", "3", "123", Permissions.VIEW_CHANNEL)
    user_data3 = add_user("three", "2", "456", Permissions.VIEW_CHANNEL)


@v1_router.post("/token", tags=["mock"])
async def mock_token(response: Response):
    set_tokens(TokenPayload(1), response)


@v1_router.post("/ban", tags=["mock"])
async def mock_ban():
    await ban_user(1)


@v1_router.post("/unban", tags=["mock"])
async def mock_unban():
    await unban_user(1)


@v1_router.post("/moderator", tags=["mock"])
async def mock_moderator():
    await make_moderator(1)


@v1_router.post("/viewer", tags=["mock"])
async def mock_viewer():
    await make_default(1)


@v1_router.post("/admin", tags=["mock"])
async def mock_admin():
    await make_admin(1)

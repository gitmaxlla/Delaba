from fastapi import APIRouter, Response, Cookie, \
                    Depends, HTTPException, Request
from fastapi.security import HTTPBearer
import jwt
import os
from copy import deepcopy
from time import time
from dotenv import load_dotenv

from ..models.users import User, Permissions
from ..core.security import validate
from ..services.users import update_user_password, \
                             mark_user_initialized, \
                             ban_user, \
                             unban_user, \
                             assign_editor, \
                             make_admin, \
                             get_user as get_user_model


DAY_SECS = 60 * 60 * 24
REFRESH_TOKEN_EXPIRES_TIME_SEC = DAY_SECS * 20
ACCESS_TOKEN_EXPIRES_TIME_SEC = 15

load_dotenv("../.env")
refresh_signature = os.getenv("JWT_REFRESH_SECRET")
access_signature = os.getenv("JWT_ACCESS_SECRET")

v1_router = APIRouter(prefix="/auth", tags=["auth"])
auth_scheme = HTTPBearer()


def require_access(request: Request) -> int:
    try:
        token = request.cookies.get("access")
        if not token:
            raise HTTPException(401, "No access token has been found.")

        credentials = dict(jwt.decode(
            token,
            access_signature,
            algorithms="HS256"))

        return credentials["id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Access token expired.")
    except Exception:
        raise HTTPException(422, "Access token is invalid.")


def require_user(id: int = Depends(require_access)) -> User:
    return get_user_model(id)


def require_edit(id: int = Depends(require_access)) -> bool:
    user = get_user_model(id)
    return user.permissions \
        & (Permissions.MANAGE_CHANNEL & Permissions.VIEW_CHANNEL) \
        == (Permissions.MANAGE_CHANNEL & Permissions.VIEW_CHANNEL)


def require_admin(id: int = Depends(require_access)) -> bool:
    user = get_user_model(id)
    print(user.permissions)
    return (user.permissions & Permissions.ADMIN) == Permissions.ADMIN


def require_refresh(request: Request) -> int:
    token = request.cookies.get("refresh")
    if not token:
        raise HTTPException(401, "No refresh token has been found.")

    credentials = None

    try:
        credentials = dict(jwt.decode(
            token,
            refresh_signature,
            algorithms="HS256"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired.")
    except Exception:
        raise HTTPException(422, "Refresh token is invalid.")

    id = int(credentials["id"])
    user = get_user_model(id)

    if user.permissions == 0:
        raise HTTPException(403, "User is currently under ban.")

    return id


@v1_router.post("/init", tags=["auth"])
async def initialize_user(id: int, init_token: str, new_password: str,
                          response: Response):
    user = get_user_model(id)
    if user.initialized:
        raise HTTPException(403, "User password has already "
                                 "been changed after account creation.")
    if validate(init_token, user.password_hashed):
        update_user_password(id, new_password)
        mark_user_initialized(id)
        generate_token_pair(id, response)
        return
    raise HTTPException(401, "Provided init token is not valid.")


@v1_router.post("/refresh", tags=["auth"])
async def refresh(response: Response, id: int = Depends(require_refresh)):
    response.set_cookie(
        key="access",
        value=get_access_token(id),
        httponly=True
    )


@v1_router.post("/login", tags=["auth"])
async def authenticate(id: int, password: str, response: Response):
    user = get_user_model(id)
    if not user.initialized:
        raise HTTPException(403, "User should change the password beforehand.")
    if validate(password, user.password_hashed):
        generate_token_pair(id, response)
    raise HTTPException(401, "Provided user password does not match.")


@v1_router.post("/mock-token", tags=["auth"])
async def mock_token(response: Response):
    generate_token_pair(1, response)


@v1_router.post("/mock-ban", tags=["auth"])
async def mock_ban():
    await ban_user(1)


@v1_router.post("/mock-editor", tags=["auth"])
async def mock_editor():
    await assign_editor(1)


@v1_router.post("/mock-viewer", tags=["auth"])
async def mock_viewer():
    await unban_user(1)


@v1_router.post("/mock-admin", tags=["auth"])
async def mock_admin():
    await make_admin(1)


def get_access_token(id: int) -> str:
    access_payload = {
        "id": id,
        "exp": int(time()) + ACCESS_TOKEN_EXPIRES_TIME_SEC,
        "type": "refresh"
    }

    access_token = jwt.encode(access_payload,
                              access_signature, algorithm="HS256")

    return access_token


def get_refresh_token(id: int) -> str:
    refresh_payload = {
        "id": id,
        "exp": int(time()) + REFRESH_TOKEN_EXPIRES_TIME_SEC,
        "type": "refresh"
    }
    refresh_token = jwt.encode(refresh_payload,
                               refresh_signature, algorithm="HS256")

    return refresh_token


def generate_token_pair(id: int, response: Response):
    response.set_cookie(
        key="refresh",
        value=get_refresh_token(id),
        httponly=True
    )

    response.set_cookie(
        key="access",
        value=get_access_token(id),
        httponly=True
    )

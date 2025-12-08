from fastapi import APIRouter, Response, \
                    Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from ..models.users import User, Permissions, Credentials, InitCredentials, \
                           has_admin_rights, has_moderator_rights, banned
from jwt import ExpiredSignatureError
from ..core.security import validate_hash, \
                            generate_access_token, \
                            generate_refresh_token, \
                            get_access_payload, \
                            get_refresh_payload
from ..services.users import update_user_password, \
                             user_by_login, \
                             mark_user_initialized, \
                             get_user as get_user_model
from ..services.tasks import get_task as get_task_model

v1_router = APIRouter(prefix="/auth", tags=["auth"])
auth_scheme = HTTPBearer()


class TokenPayload:
    __slots__ = ("id")

    def __init__(self, id):
        self.id = id


def require_access(request: Request) -> User:
    try:
        token = request.cookies.get("access")
        if not token:
            raise HTTPException(401, "No access token has been found.")

        credentials = get_access_payload(token)

        return get_user_model(credentials["id"])
    except ExpiredSignatureError:
        raise HTTPException(401, "Access token expired.")
    except Exception:
        raise HTTPException(422, "Access token is invalid.")


def require_refresh(request: Request) -> User:
    token = request.cookies.get("refresh")
    if not token:
        raise HTTPException(401, "No refresh token has been found.")

    credentials = None

    try:
        credentials = get_refresh_payload(token)
    except ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired.")
    except Exception:
        raise HTTPException(422, "Refresh token is invalid.")

    id = int(credentials["id"])
    user = get_user_model(id)

    if banned(user):
        raise HTTPException(403, "User is currently under ban.")

    return user


@v1_router.post("/init", tags=["auth"])
async def initialize_user(credentials: InitCredentials,
                          response: Response) -> None:
    user = user_by_login(credentials.login)
    if user.initialized:
        raise HTTPException(403, "User password has already "
                                 "been changed after account creation.")
    if validate_hash(credentials.init_token, user.password_hashed):
        update_user_password(user.id, credentials.new_password)
        mark_user_initialized(user.id)
        set_tokens(TokenPayload(user.id), response)
        return
    raise HTTPException(401, "Provided init token is not valid.")


@v1_router.post("/login", tags=["auth"])
async def authenticate_user(
        credentials: Credentials, response: Response) -> None:
    user: User = user_by_login(credentials.login)

    if not user:
        raise HTTPException(404, "User not found.")
    elif not user.initialized:
        raise HTTPException(403, "User should change the password beforehand.")
    elif banned(user):
        raise HTTPException(403, "User is banned.")

    if validate_hash(credentials.password, user.password_hashed):
        set_tokens(TokenPayload(user.id), response)
    else:
        raise HTTPException(401, "Provided user password does not match.")


@v1_router.post("/refresh", tags=["auth"])
async def refresh_access_token(response: Response,
                               user: User = Depends(require_refresh)) -> None:
    response.set_cookie(
        key="access",
        value=generate_access_token(user.id),
        httponly=True
    )


def set_tokens(payload: TokenPayload, response: Response) -> None:
    response.set_cookie(
        key="refresh", httponly=True,
        value=generate_refresh_token(payload.id))

    response.set_cookie(
        key="access", httponly=True,
        value=generate_access_token(payload.id))


def logged_in(user: User = Depends(require_access)) -> User:
    return user


def moderator(user: User = Depends(logged_in)) -> User:
    if not has_admin_rights(user) and not has_moderator_rights(user):
        raise HTTPException(403, "Insufficient rights.")
    return user


def admin(user: User = Depends(logged_in)) -> User:
    if not has_admin_rights(user):
        raise HTTPException(403, "Insufficient rights.")
    return user


def owns_channel(user: User = Depends(moderator)) -> str:
    res = None
    if has_admin_rights(user):
        res = ""
    elif has_moderator_rights(user):
        res = user.channel
    return res


def manages_user_id(id: int, user: User = Depends(moderator)) -> User:
    if id == user.id:
        raise HTTPException(403, "Cannot manage themselves.")

    if (not has_admin_rights(user)
       and get_user_model(id).channel != user.channel):
        raise HTTPException(403, "Insufficient rights.")

    return user


def task_id_reachable(id: int, user: User = Depends(logged_in)) -> User:
    if not has_admin_rights(user) \
       and get_task_model(id).channel != user.channel:
        raise HTTPException(403, "Insufficient rights.")
    return user

import math
from typing import Any, List, Optional

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound

from src.core.permissions import PermissionTags
from src.core.security import generate_password, validate_hash
from src.core.security import hash as pwdlib_hash
from src.database import db
from src.models.users import User as UserModel
from src.schemas.users import User as UserSchema, UsersPaginatedResponse
from src.services.mail import send_login_details


def delete_user(id: int):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        session.delete(user)


def update_user_data(id: int, data: dict):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.data = data


def get_user_permissions(id: int) -> Optional[PermissionTags]:
    with db.Session() as session:
        user = session.get(UserModel, id)
        if user:
            return user.permissions
        return None


def get_user_data(id: int) -> dict[str, Any]:
    data = {}

    with db.Session() as session:
        user = session.get(UserModel, id)
        if user and user.data:
            data = user.data

    return data


def update_user_password(id, new_password):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.password_hashed = pwdlib_hash(new_password)


def mark_user_initialized(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.initialized = True


async def ban_user(id):
    if id == 0:
        return

    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.permissions = user.permissions & PermissionTags.BANNED


async def transfer_user(id: int, channel: str):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.channel = channel


async def unban_user(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.permissions = user.permissions & (~PermissionTags.BANNED)


async def make_admin(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.channel = ""
            user.permissions = (
                PermissionTags.VIEW_CHANNEL
                | PermissionTags.ADMIN
                | PermissionTags.MANAGE_CHANNEL
            )


async def make_default(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.permissions = PermissionTags.VIEW_CHANNEL


async def make_moderator(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.permissions = (
                PermissionTags.VIEW_CHANNEL | PermissionTags.MANAGE_CHANNEL
            )


def add_user(login: str, role: str, channel: str, permissions: PermissionTags):
    init_password = generate_password()

    user = UserModel(
        login=login,
        role=role,
        permissions=permissions,
        password_hashed=pwdlib_hash(init_password),
        channel=channel,
    )

    with db.Session() as session:
        session.add(user)
        session.flush()
        session.refresh(user)
        session.commit()

    send_login_details(login, init_password)


def log_in(login: str, password: str) -> tuple[UserSchema, bool]:
    query = select(UserModel).where(UserModel.login == login)
    data = db.Session().execute(query)
    try:
        user = data.scalar_one()
        success = validate_hash(password, user.password_hashed)
        return UserSchema.model_validate(user), success
    except NoResultFound:
        raise HTTPException(404, "No user with such login found.")


def get_user(id: int) -> Optional[UserSchema]:
    try:
        with db.Session() as session:
            user = session.get(UserModel, id)
            if user:
                return UserSchema.model_validate(user)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"User (id={id}) not found")


def get(
    channel: list[str],
    role: list[str] | None,
    permissions: list[int] | None,
    q: str | None,
    email: str | None,
    newest_first: bool | None,
    page: int,
    page_size: int,
) -> UsersPaginatedResponse:
    users: list[UserSchema] = []

    with db.Session() as session:
        query = select(UserModel).order_by(
            UserModel.id.asc() if newest_first else UserModel.id.desc()
        )

        if q and q != "":
            query = query.where(
                UserModel.login.ilike(f"%{q}%") | UserModel.role.ilike(f"%{q}%")
            )

        query = query.where(UserModel.channel.in_(channel))

        if email:
            query = query.where(UserModel.login == email)

        if role:
            query = query.where(UserModel.role.in_(role))

        if permissions:
            query = query.where(UserModel.permissions.in_(permissions))

        count_q = select(func.count()).select_from(query.subquery())
        count = session.execute(count_q).scalar()
        if not count:
            count = 0
        total = count

        query = query.slice(page * page_size, (page + 1) * page_size)
        user_models = session.scalars(query).all()
        users = [UserSchema.model_validate(user) for user in user_models]

        return UsersPaginatedResponse(
            values=users,
            total=int(total),
        )


def get_all_users() -> List[UserSchema]:
    with db.Session() as session:
        users = session.query(UserModel).all()
        return [UserSchema.model_validate(user) for user in users]

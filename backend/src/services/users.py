from typing import List, cast

from src.database import db
from src.models.users import User as UserModel
from src.schemas.users import User as UserSchema

from src.services.mail import send_login_details
from src.core.security import hash as pwdlib_hash, generate_password
from src.core.permissions import Permissions, to_binstr
from src.adapters.sqlalchemy_pydantic import to_user_schema

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from fastapi import HTTPException


def delete_user(id: int):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        session.delete(user)


def update_user_data(id: int, data: dict):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        if user:
            user.data = data


def get_user_permissions(id: int) -> int:
    with db.Session() as session:
        user = session.get(UserModel, id)
        session.commit()
        session.refresh(user)

        if user:
            return int(user.permissions, 2)
        return 0


def get_user_data(id: int) -> dict:
    data = {}

    with db.Session() as session:
        user = session.get(UserModel, id)
        if user:
            data = user.data.__dict__

    return data


def update_user_password(id, new_password):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        user.password_hashed = pwdlib_hash(new_password)


def mark_user_initialized(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        user.initialized = True


async def ban_user(id):
    if id == 0:
        return

    with db.Session() as session:
        user = session.get(UserModel, id)
        user.permissions = to_binstr(int(user.permissions, 2) & Permissions.BANNED)
        session.commit()


async def transfer_user(id: int, channel: str):
    with db.Session() as session:
        user = session.get(UserModel, id)
        user.channel = channel
        session.commit()


async def unban_user(id):
    with db.Session() as session:
        user = session.get(UserModel, id)
        user.permissions = to_binstr(int(user.permissions, 2) & (~Permissions.BANNED))
        session.commit()


async def make_admin(id):
    with db.Session() as session:
        user = session.get(UserModel, id)
        user.permissions = to_binstr(
            Permissions.VIEW_CHANNEL | Permissions.ADMIN | Permissions.MANAGE_CHANNEL
        )
        user.channel = ""
        session.commit()


async def make_default(id):
    with db.Session() as session:
        user = session.get(UserModel, id)
        user.permissions = to_binstr(Permissions.VIEW_CHANNEL)
        session.commit()


async def make_moderator(id):
    with db.Session.begin() as session:
        user = session.get(UserModel, id)
        user.permissions = to_binstr(
            Permissions.VIEW_CHANNEL | Permissions.MANAGE_CHANNEL
        )


def add_user(login: str, role: str, channel: str, permissions: Permissions):
    init_password = generate_password()

    user = UserModel(
        login=login,
        role=role,
        permissions=to_binstr(permissions),
        password_hashed=pwdlib_hash(init_password),
        channel=channel,
    )

    with db.Session() as session:
        session.add(user)
        session.flush()
        session.refresh(user)
        session.commit()

    send_login_details(login, init_password)


def user_by_login(value: str) -> UserModel:
    query = select(UserModel).where(UserModel.login == value)
    data = db.Session().execute(query)

    try:
        return data.scalar_one()
    except NoResultFound:
        raise HTTPException(404, "No user with such login found.")


def get_user(id: int) -> UserSchema:
    try:
        with db.Session() as session:
            user = cast(UserModel, session.get(UserSchema, id))
        return to_user_schema(user)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"User (id={id}) not found")


def get_by_channel(channel: str, page: int, page_size: int) -> List[UserSchema]:
    users = []

    with db.Session() as session:
        query = select(UserModel)
        if channel != "":
            query = query.where(UserModel.channel == channel)
        query = query.offset(page * page_size).limit(page_size)
        users = session.scalars(query).all()

    return [to_user_schema(user) for user in users]


def get_all_users() -> List[UserSchema]:
    with db.Session() as session:
        users = session.query(UserModel).all()
    return [to_user_schema(user) for user in users]

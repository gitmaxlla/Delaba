from typing import List
import math

from ..database import db
from ..schemas.users import User as UserSchema, \
    Permissions, user_from_schema

from ..core.security import generate_uuid, hash as pwdlib_hash
from ..models.users import User as UserModel, UserCreationResponse
from ..internal.root import ADMIN_INIT_TOKEN

from ..schemas.channels import Channel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from fastapi import HTTPException


def delete_user(id: int):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        session.delete(user)
        session.commit()


def update_user_data(user: UserModel, data: dict):
    with db.Session() as session:
        db_user = session.get(UserSchema, user.id)
        db_user.data = data
        session.commit()


def get_user_data(user: UserModel) -> dict:
    data = {}

    with db.Session() as session:
        db_user = session.get(UserSchema, user.id)
        session.flush()
        session.refresh(db_user)

        data = db_user.data

    return data


def update_user_password(id, new_password):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.password_hashed = pwdlib_hash(new_password)
        session.commit()


def mark_user_initialized(id):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.initialized = True
        session.commit()


async def ban_user(id):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.permissions = permissions_to_db(
            int(user.permissions, 2) & Permissions.BANNED)
        session.commit()


async def transfer_user(id: int, channel: str):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.channel = channel
        session.commit()


async def unban_user(id):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.permissions = permissions_to_db(
            int(user.permissions, 2) & (~Permissions.BANNED))
        session.commit()


async def make_admin(id):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.permissions = permissions_to_db(
            Permissions.VIEW_CHANNEL
            | Permissions.ADMIN
            | Permissions.MANAGE_CHANNEL)
        user.channel = ""
        session.commit()


async def make_default(id):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.permissions = permissions_to_db(Permissions.VIEW_CHANNEL)
        session.commit()


async def make_moderator(id):
    with db.Session() as session:
        user = session.get(UserSchema, id)
        user.permissions = \
            permissions_to_db(
                Permissions.VIEW_CHANNEL
                | Permissions.MANAGE_CHANNEL)
        session.commit()


def permissions_to_db(permissions: int) -> str:
    permission_bits_len = 2 + math.floor(math.log(max(Permissions) + 1))
    return str.zfill(bin(permissions)[2:],
                     permission_bits_len)


def add_user(login: str, role: str,
             channel: str, permissions: Permissions) -> UserCreationResponse:
    init_token = generate_uuid()

    user = UserSchema(
                login=login,
                role=role,
                permissions=permissions_to_db(permissions),
                password_hashed=pwdlib_hash(init_token),
                channel=channel)

    id = None

    with db.Session() as session:
        session.add(user)
        session.flush()
        session.refresh(user)

        id = user.id
        session.commit()

    return UserCreationResponse(id=id, init_token=init_token)


def user_by_login(login: str) -> UserModel:
    query = select(UserSchema).where(UserSchema.login == login)
    data = db.Session().execute(query)
    return user_from_schema(data.scalar_one())


def get_user(id: int) -> UserModel:
    try:
        with db.Session() as session:
            user = session.get(UserSchema, id)
        return user_from_schema(user)
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"User (id={id}) not found")


def create_admin_user():
    user = UserSchema(
                id=0,
                login="",
                role="Администратор",
                permissions=permissions_to_db(
                    Permissions.ADMIN
                    | Permissions.MANAGE_CHANNEL
                    | Permissions.VIEW_CHANNEL
                ),
                password_hashed=pwdlib_hash(ADMIN_INIT_TOKEN),
                channel="")

    with db.Session() as session:
        session.merge(Channel(name=""))
        session.commit()

    with db.Session() as session:
        session.merge(user)
        session.commit()


def get_by_channel(channel: str) -> List[UserModel]:
    users = []

    with db.Session() as session:
        query = select(UserSchema)
        if channel != "":
            query = query \
                .where(UserSchema.channel == channel)
        users = session.scalars(query).all()

    return [user_from_schema(user) for user in users]


def get_all_users() -> List[UserModel]:
    with db.Session() as session:
        users = session.query(UserSchema).all()
    return [user_from_schema(user) for user in users]

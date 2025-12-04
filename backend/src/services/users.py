from ..database import db
from ..schemas.users import User, Permissions, user_from_schema
from typing import List

from ..core.security import generate_uuid, hash as pwdlib_hash
import math
from ..models.users import User as UserModel


def get_all_users() -> List[UserModel]:
    with db.Session() as session:
        users = session.query(User).all()
    return [user_from_schema(user) for user in users]


def permissions_to_db(permissions: int) -> str:
    permission_bits_len = 2 + math.floor(math.log(max(Permissions) + 1))
    return str.zfill(bin(permissions)[2:],
                     permission_bits_len)


def delete_all_users():
    with db.Session() as session:
        session.query(User).delete()
        session.commit()


def add_an_user(name: str, channel: str):
    initial_access_code = generate_uuid()

    user = User(name=name,
                permissions=permissions_to_db(Permissions.VIEW_CHANNEL),
                password_hashed=pwdlib_hash(initial_access_code),
                channel=channel)

    id = -1

    with db.Session() as session:
        session.add(user)
        session.flush()
        session.refresh(user)

        id = user.id
        session.commit()

    return {"id": id, "init_token": initial_access_code}


def get_user(id: int) -> UserModel | None:
    user = None
    with db.Session() as session:
        user = session.get(User, id)
    return user_from_schema(user)


def delete_user(id):
    with db.Session() as session:
        user = session.get(User, id)
        session.delete(user)
        session.commit()


def update_user_data(id, data):
    with db.Session() as session:
        user = session.get(User, id)
        user.data = data
        session.commit()


def update_user_password(id, new_password):
    with db.Session() as session:
        user = session.get(User, id)
        user.password_hashed = new_password
        session.commit()


def mark_user_initialized(id):
    with db.Session() as session:
        user = session.get(User, id)
        user.initialized = True
        session.commit()


async def ban_user(id):
    with db.Session() as session:
        user = session.get(User, id)
        user.permissions = permissions_to_db(0)
        session.commit()


async def assign_editor(id):
    with db.Session() as session:
        user = session.get(User, id)
        user.permissions = \
            permissions_to_db(
                Permissions.VIEW_CHANNEL
                | Permissions.MANAGE_CHANNEL)
        session.commit()


async def unban_user(id):
    with db.Session() as session:
        user = session.get(User, id)
        user.permissions = permissions_to_db(Permissions.VIEW_CHANNEL)
        session.commit()


async def make_admin(id):
    with db.Session() as session:
        user = session.get(User, id)
        user.permissions = permissions_to_db(
            Permissions.VIEW_CHANNEL
            | Permissions.ADMIN
            | Permissions.MANAGE_CHANNEL)
        session.commit()

import math
from enum import IntFlag


class Permissions(IntFlag):
    BANNED = 1
    VIEW_CHANNEL = 2
    MANAGE_CHANNEL = 4
    ADMIN = 8


def has_moderator_rights(p: Permissions) -> bool:
    return (p & Permissions.MANAGE_CHANNEL) == Permissions.MANAGE_CHANNEL


def has_admin_rights(p: Permissions) -> bool:
    return (p & Permissions.ADMIN) == Permissions.ADMIN


def banned(p: Permissions) -> bool:
    return (p & Permissions.BANNED) == Permissions.BANNED


def to_binstr(permissions: int) -> str:
    permission_bits_len = 2 + math.floor(math.log(max(Permissions) + 1))
    return str.zfill(bin(permissions)[2:], permission_bits_len)

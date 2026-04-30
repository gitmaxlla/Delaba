import math
from enum import IntFlag
from typing import Optional, Any

from sqlalchemy import Dialect
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.types import String, TypeDecorator, TypeEngine


class PermissionTags(IntFlag):
    BANNED = 1
    VIEW_CHANNEL = 2
    MANAGE_CHANNEL = 4
    ADMIN = 8


class Permissions(TypeDecorator[PermissionTags]):
    impl = BIT
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        if dialect.name == "sqlite":
            return String().dialect_impl(dialect)
        return super().load_dialect_impl(dialect)

    def __init__(self):
        self.bitlen = int(1 + math.floor(math.log(max(PermissionTags), 2)))
        super().__init__(length=self.bitlen, varying=False)

    def process_bind_param(
        self, value: Optional[PermissionTags], dialect: Dialect
    ) -> Optional[str]:
        if not value:
            return None
        return self._to_binstr(value)

    def process_result_value(
        self, value: Optional[str], dialect: Dialect
    ) -> Optional[PermissionTags]:
        if not value:
            return None
        return PermissionTags(int(value, 2))

    def _to_binstr(self, value: int) -> str:
        return str.zfill(bin(value)[2:], self.bitlen)


def has_moderator_rights(p: PermissionTags) -> bool:
    return (p & PermissionTags.MANAGE_CHANNEL) != 0


def has_admin_rights(p: PermissionTags) -> bool:
    return (p & PermissionTags.ADMIN) != 0


def banned(p: PermissionTags) -> bool:
    return (p & PermissionTags.BANNED) != 0

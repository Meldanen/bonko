from dataclasses import dataclass

from enums.RoleEnum import RoleEnum


@dataclass
class User:
    id: int
    permission_level: RoleEnum

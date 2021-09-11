from dataclasses import dataclass

from enums.RoleEnum import RoleEnum


@dataclass
class Command:
    id: int
    command: str
    permission: RoleEnum
    example: str

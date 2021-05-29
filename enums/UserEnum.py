from dataclasses import dataclass
from enum import Enum

from enums.PermissionsEnum import PermissionsEnum


@dataclass
class User:
    id: int
    permission_level: PermissionsEnum


class UserEnum(Enum):
    GIANNAKIS = User(294577564603645952, PermissionsEnum.PUBLIC)

    MELDANEN = User(164447968332611584, PermissionsEnum.DEVELOPER)

    MELON = User(186521813285601280, PermissionsEnum.ADMIN)

    JOSEPH = User(173766017258881024, PermissionsEnum.ADMIN)

    @staticmethod
    def is_good_person(id: int) -> bool:
        return id in [UserEnum.MELDANEN.value.id, UserEnum.JOSEPH.value.id, UserEnum.MELON.value.id]

    @staticmethod
    def is_giannakis(id: int) -> bool:
        return id == UserEnum.GIANNAKIS.value.id

    @staticmethod
    def is_megus(id: int) -> bool:
        return id == UserEnum.MELDANEN.value.id

    @staticmethod
    def is_melon(id: int) -> bool:
        return id == UserEnum.MELON.value.id

from dataclasses import dataclass
from enum import Enum

from enums.RoleEnum import RoleEnum


@dataclass
class User:
    id: int
    permission_level: RoleEnum


class UserEnum(Enum):
    GIANNAKIS = User(294577564603645952, RoleEnum.PUBLIC)

    MELDANEN = User(164447968332611584, RoleEnum.MEGUS)

    MELON = User(186521813285601280, RoleEnum.ADMIN)

    JOSEPH = User(173766017258881024, RoleEnum.ADMIN)

    SIBLING = User(319171521354530818, RoleEnum.RESTRICTED)

    CON = User(318437163169611776, RoleEnum.RESTRICTED)

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

    @staticmethod
    def get_from_id(id):
        for user in UserEnum:
            if user.value.id == id:
                return user.value
        return None

from dataclasses import dataclass
from enum import Enum
from typing import List

from enums.RoleEnum import RoleEnum


@dataclass
class User:
    id: int
    permission_level: RoleEnum


class UserEnum(Enum):
    GIANNAKIS = User(294577564603645952, RoleEnum.PLEB)

    BONKO = User(842351473408344064, RoleEnum.ADMIN)

    ANTI_BONKO = User(879640212697931786, RoleEnum.ADMIN)

    MELDANEN = User(164447968332611584, RoleEnum.MEGUS)

    MELON = User(186521813285601280, RoleEnum.ADMIN)

    JOSEPH = User(173766017258881024, RoleEnum.ADMIN)

    SIBLING = User(319171521354530818, RoleEnum.RESTRICTED)

    CON = User(318437163169611776, RoleEnum.RESTRICTED)

    SIBLINGS_SIBLING = User(181353937662771200, RoleEnum.PLEB)

    NYROID = User(318425980073148418, RoleEnum.PLEB)

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
    def is_bonko(id: int) -> bool:
        return id == UserEnum.BONKO.value.id

    @staticmethod
    def is_melon(id: int) -> bool:
        return id == UserEnum.MELON.value.id

    @staticmethod
    def is_nyroid(id: int) -> bool:
        return id == UserEnum.NYROID.value.id

    @staticmethod
    def is_anti_bonko(id: int) -> bool:
        return id == UserEnum.ANTI_BONKO.value.id

    @staticmethod
    def get_from_id(id):
        for user in UserEnum:
            if user.value.id == id:
                return user.value
        return None

    @staticmethod
    async def get_user_id(members: List, username: str) -> int:
        for member in members:
            if username.lower() in member.name.lower():
                return member.id

    @staticmethod
    async def get_user(members: List, username: str, mention: bool) -> str:
        if mention:
            user_id = await UserEnum.get_user_id(members, username)
            return UserEnum.format_user_id_for_mention(str(user_id))
        else:
            return username

    @staticmethod
    async def get_giannakis(mention: bool) -> str:
        if mention:
            return UserEnum.format_user_id_for_mention(str(UserEnum.GIANNAKIS.value))
        else:
            return "giannaki"

    @staticmethod
    def format_user_id_for_mention(user_id: str) -> str:
        return "<@!" + user_id + ">"

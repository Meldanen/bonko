from enum import Enum


class UserEnum(Enum):

    GIANNAKIS = 294577564603645952

    MELDANEN = 164447968332611584

    MELON = 186521813285601280

    JOSEPH = 173766017258881024

    @staticmethod
    def is_good_person(id: int) -> bool:
        return id in [UserEnum.MELDANEN.value, UserEnum.JOSEPH.value, UserEnum.MELON.value]

    @staticmethod
    def is_giannakis(id: int) -> bool:
        return id == UserEnum.GIANNAKIS.value

    @staticmethod
    def is_megus(id: int) -> bool:
        return id == UserEnum.MELDANEN.value

    @staticmethod
    def is_melon(id: int) -> bool:
        return id == UserEnum.MELON.value

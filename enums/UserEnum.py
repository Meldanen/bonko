from enum import Enum


class UserEnum(Enum):

    GIANNAKIS = 294577564603645952

    MELDANEN = 164447968332611584

    HELEN = 186521813285601280

    JOSEPH = 173766017258881024

    @staticmethod
    def is_good_person(id):
        return id == UserEnum.MELDANEN.value or id == UserEnum.JOSEPH.value or id == UserEnum.HELEN.value

    @staticmethod
    def is_giannakis(id):
        return id == UserEnum.GIANNAKIS.value

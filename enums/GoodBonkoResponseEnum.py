from dataclasses import dataclass
from enum import Enum
from random import randrange

from utils import FileUtils


@dataclass
class GoodBonkoResponse:
    id: int
    value: str
    file: bool


class GoodBonkoResponseEnum(Enum):
    FLOWER = GoodBonkoResponse(0, "(✿◠‿◠)", False)

    GOOFY = GoodBonkoResponse(1, "assets/gifs/shy_goofy.gif", True)

    @staticmethod
    def get_random_response():
        index = randrange(len(GoodBonkoResponseEnum))
        return GoodBonkoResponseEnum.get_response(index)

    @staticmethod
    def get_response(id):
        response = GoodBonkoResponseEnum.get_by_id(id).value
        if response.file:
            return FileUtils.get_file(response.value)
        return response.value

    @staticmethod
    def get_by_id(id):
        for enum in GoodBonkoResponseEnum:
            if enum.value.id == id:
                return enum

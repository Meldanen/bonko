from dataclasses import dataclass
from enum import Enum
from random import randrange, choice

from utils import FileUtils


@dataclass
class JudgeBonkoResponse:
    id: int
    value: str
    file: bool


class JudgeBonkoResponseEnum(Enum):
    FLOWER = JudgeBonkoResponse(0, "(✿◠‿◠)", False)

    GOOFY = JudgeBonkoResponse(1, "assets/gifs/shy_goofy.gif", True)

    SAD = JudgeBonkoResponse(2, "（´＿｀）", False)

    @staticmethod
    def get_random_response():
        index = randrange(len(JudgeBonkoResponseEnum))
        return JudgeBonkoResponseEnum.get_response(index)

    @staticmethod
    def get_random_happy_response():
        happy_responses = [0, 1]
        index = choice(happy_responses)
        return JudgeBonkoResponseEnum.get_response(index)

    @staticmethod
    def get_random_sad_response():
        sad_responses = [2]
        index = choice(sad_responses)
        return JudgeBonkoResponseEnum.get_response(index)

    @staticmethod
    def get_response(id):
        response = JudgeBonkoResponseEnum.get_by_id(id).value
        if response.file:
            return FileUtils.get_file(response.value)
        return response.value

    @staticmethod
    def get_by_id(id):
        for enum in JudgeBonkoResponseEnum:
            if enum.value.id == id:
                return enum

from enum import Enum

from beans.GrammarCategory import GrammarCategory

FEWER_STRING = "fewer"
LESS_STRING = "less"


class GrammarEnum(Enum):
    CASING = GrammarCategory(0, "CASING")

    GRAMMAR = GrammarCategory(1, "GRAMMAR")

    @staticmethod
    def is_casing(id: int) -> bool:
        return id == GrammarEnum.CASING.value.id

    @staticmethod
    def is_grammar(id: int) -> bool:
        return id == GrammarEnum.GRAMMAR.value.id

    @staticmethod
    def is_fewer(message: str) -> bool:
        return FEWER_STRING in message.lower()

    @staticmethod
    def is_less(message: str) -> bool:
        return LESS_STRING in message.lower()

    @staticmethod
    def is_fewer_in_replacements(replacements: list()) -> bool:
        return GrammarEnum.is_string_in_replacements(FEWER_STRING, replacements)

    @staticmethod
    def is_less_in_replacements(replacements: list()) -> bool:
        return GrammarEnum.is_string_in_replacements(LESS_STRING, replacements)

    @staticmethod
    def is_string_in_replacements(target_string: str, replacements: list()) -> bool:
        return map(lambda replacement: target_string in replacement.lower, replacements)

    @staticmethod
    def get_from_value(value):
        for enum in GrammarEnum:
            if enum.value.value.lower() == value.lower():
                return enum
        return None

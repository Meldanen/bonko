from enum import Enum


class CommandsEnum(Enum):
    BONK = "bonk"

    SPAM_SOFT = "spam"

    SPAM_HARD = "spamhard"

    BAD_GIANNAKIS = "badgiannakis"

    WORD_OF_THE_DAY = "wordoftheday"

    PERMISSIONS = "permissions"

    ALLOW_SPAM = "allowspam"

    DISALLOW_SPAM = "disallowspam"

    ASTONISHED = "astonished"

    SHRUG = "shrug"

    YE = "ye"

    ART = "art"

    @staticmethod
    def is_allow_spam(permission: str) -> bool:
        return permission == CommandsEnum.ALLOW_SPAM.value

    @staticmethod
    def is_disallow_spam(permission: str) -> bool:
        return permission == CommandsEnum.DISALLOW_SPAM.value

    @staticmethod
    def is_spam_related(permission: str) -> bool:
        return CommandsEnum.is_allow_spam(permission) or CommandsEnum.is_disallow_spam(permission)

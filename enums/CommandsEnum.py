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

    @staticmethod
    def is_allow_spam(permission):
        return permission == CommandsEnum.ALLOW_SPAM.value

    @staticmethod
    def is_disallow_spam(permission):
        return permission == CommandsEnum.DISALLOW_SPAM.value

    @staticmethod
    def is_spam_related(permission):
        return CommandsEnum.is_allow_spam(permission) or CommandsEnum.is_disallow_spam(permission)

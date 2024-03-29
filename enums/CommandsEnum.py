from enum import Enum

from beans.Command import Command
from enums.RoleEnum import RoleEnum


class CommandsEnum(Enum):
    BONK = Command(0, "bonk", RoleEnum.PLEB, ";;bonk")

    OMEGA_BONK = Command(1, "omegabonk", RoleEnum.PLEB, ";;omegabonk")

    SPAM_SOFT = Command(2, "spam", RoleEnum.RESTRICTED, ";;spam <emoji> <times_to_spam> <user>")

    SPAM_HARD = Command(3, "spamhard", RoleEnum.DEVELOPER, ";;spamhard <emoji> <times_to_spam> <user>")

    BAD_GIANNAKIS = Command(4, "badgiannakis", RoleEnum.DEVELOPER, ";;badgiannakis")

    WORD_OF_THE_DAY = Command(5, "wordoftheday", RoleEnum.PLEB, ";;wordoftheday")

    PERMISSIONS = Command(6, "permissions", RoleEnum.DEVELOPER, ";;permissions <permission_type> <user>")

    ALLOW_SPAM = Command(7, "allowspam", RoleEnum.DEVELOPER, ";;permissions allowspam <user>")

    DISALLOW_SPAM = Command(8, "disallowspam", RoleEnum.DEVELOPER, ";;permissions disallowspam <user>")

    ASTONISHED = Command(9, "astonished", RoleEnum.PLEB, ";;astonished <optional:naked>")

    SHRUG = Command(10, "shrug", RoleEnum.PLEB, ";;shrug")

    YE = Command(11, "ye", RoleEnum.PLEB, "ye")

    ART = Command(12, "art", RoleEnum.PLEB, ";;art <optional:emojis>")

    LEMONARIS = Command(13, "lemonaris", RoleEnum.PLEB, ";;lemonaris <optional:emojis>")

    RANDOM_MESSAGE = Command(14, "randommessage", RoleEnum.MEGUS, "N/A")

    HAXOR = Command(15, "haxor", RoleEnum.MEGUS, ";;haxor <code> <optional:post_to_server>")

    HELP = Command(16, "help", RoleEnum.PLEB, ";;help")

    SAY = Command(17, "say", RoleEnum.MEGUS, "N/A")

    QUOTE = Command(18, "quote", RoleEnum.PLEB, ";;quote <optional:number>")

    WAR_CRIMES = Command(19, "warcrimes", RoleEnum.PLEB, ";;warcrimes <optional:cheese>")

    SALT = Command(20, "salt", RoleEnum.PLEB, ";;salt")

    REACT_MODE = Command(21, "reactmode", RoleEnum.PLEB, ";;reactmode <on:off> <emojis>")

    SALT_MODE = Command(22, "saltmode", RoleEnum.PLEB, ";;saltmode <on:off>")

    GARIDAKI = Command(23, "garidaki", RoleEnum.PLEB, ";;garidaki")

    COQ = Command(24, "coq", RoleEnum.PLEB, ";;coq")

    HIVE_MIND = Command(25, "hivemind", RoleEnum.PLEB, ";;hivemind")

    OH_YOU = Command(26, "ohyou", RoleEnum.PLEB, ";;ohyou")

    FAITH = Command(27, "faith", RoleEnum.PLEB, ";;faith")

    BELOVED = Command(28, "beloved", RoleEnum.PLEB, ";;beloved")

    @staticmethod
    def is_allow_spam(permission: str) -> bool:
        return permission == CommandsEnum.ALLOW_SPAM.value.command

    @staticmethod
    def is_disallow_spam(permission: str) -> bool:
        return permission == CommandsEnum.DISALLOW_SPAM.value.command

    @staticmethod
    def is_spam_related(permission: str) -> bool:
        return CommandsEnum.is_allow_spam(permission) or CommandsEnum.is_disallow_spam(permission)

    @staticmethod
    def format_displays_for_help_command(permission_level):
        displays = CommandsEnum.get_all_display_for_help_command(permission_level)
        message = ""
        for display in displays:
            message += f'\n{display}'
        return message

    @staticmethod
    def get_all_display_for_help_command(role):
        help_message = list()
        for enum in CommandsEnum.get_commands_of_specific_role(role):
            help_message.append(CommandsEnum.get_display_for_help_command(enum))
        return help_message

    @staticmethod
    def get_commands_of_specific_role(role):
        available_levels = RoleEnum.get_available_levels(role)
        available_commands = list()
        for enum in CommandsEnum:
            if enum.value.permission in available_levels:
                available_commands.append(enum)
        return available_commands

    @staticmethod
    def get_display_for_help_command(commands_enum):
        command = commands_enum.value
        return f'{command.command.capitalize()}: Permission: {command.permission.value.capitalize()}, Example: {command.example}'

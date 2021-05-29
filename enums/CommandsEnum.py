from dataclasses import dataclass
from enum import Enum

from enums.PermissionsEnum import PermissionsEnum


@dataclass
class Command:
    id: int
    command: str
    permission: PermissionsEnum
    example: str


class CommandsEnum(Enum):
    BONK = Command(0, "bonk", PermissionsEnum.PUBLIC, ";;bonk")

    OMEGA_BONK = Command(1, "omegabonk", PermissionsEnum.PUBLIC, ";;omegabonk")

    SPAM_SOFT = Command(2, "spam", PermissionsEnum.RESTRICTED, ";;spam <emoji> <times_to_spam> <user>")

    SPAM_HARD = Command(3, "spamhard", PermissionsEnum.DEVELOPER, ";;spamhard <emoji> <times_to_spam> <user>")

    BAD_GIANNAKIS = Command(4, "badgiannakis", PermissionsEnum.DEVELOPER, ";;badgiannakis")

    WORD_OF_THE_DAY = Command(5, "wordoftheday", PermissionsEnum.PUBLIC, ";;wordoftheday")

    PERMISSIONS = Command(6, "permissions", PermissionsEnum.DEVELOPER, ";;permissions <permission_type> <user>")

    ALLOW_SPAM = Command(7, "allowspam", PermissionsEnum.DEVELOPER, ";;permissions allowspam <user>")

    DISALLOW_SPAM = Command(8, "disallowspam", PermissionsEnum.DEVELOPER, ";;permissions disallowspam <user>")

    ASTONISHED = Command(9, "astonished", PermissionsEnum.PUBLIC, ";;astonished <optional:naked")

    SHRUG = Command(10, "shrug", PermissionsEnum.PUBLIC, ";;shrug")

    YE = Command(11, "ye", PermissionsEnum.PUBLIC, ";;ye")

    ART = Command(12, "art", PermissionsEnum.PUBLIC, ";;art <optional:emoji>")

    LEMONARIS = Command(13, "lemonaris", PermissionsEnum.PUBLIC, ";;lemonaris <optional:emoji>")

    RANDOM_MESSAGE = Command(14, "randommessage", PermissionsEnum.PUBLIC, "N/A")

    HAXOR = Command(15, "haxor", PermissionsEnum.DEVELOPER, ";;haxor <code> <optional:post_to_server>")

    HELP = Command(16, "help", PermissionsEnum.PUBLIC, ";;help")

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
    def get_all_display_for_help_command(permission_level):
        help_message = list()
        for enum in CommandsEnum.get_all_of_specific_permission_level(permission_level):
            help_message.append(CommandsEnum.get_display_for_help_command(enum))
        return help_message

    @staticmethod
    def get_all_of_specific_permission_level(permission_level):
        available_levels = PermissionsEnum.get_available_levels(permission_level)
        available_commands = list()
        for enum in CommandsEnum:
            if enum.value.permission in available_levels:
                available_commands.append(enum)
        return available_commands


    @staticmethod
    def get_display_for_help_command(commands_enum):
        command = commands_enum.value
        return f'Command: {command.command.capitalize()}, Permission: {command.permission.value.capitalize()}, Example: {command.example}'


if __name__ == '__main__':
    print(CommandsEnum.get_all_display_for_help_command(PermissionsEnum.DEVELOPER))

from enums.CommandsEnum import CommandsEnum
from enums.RoleEnum import RoleEnum
from enums.UserEnum import UserEnum


class PermissionService:

    def __init__(self, bot_id, logging_service):
        self.bot_id = bot_id
        self.logging_service = logging_service

    def is_allowed_to_use_command(self, user_id, command, special_permissions):
        if PermissionService.is_bonko(user_id):
            return
        user = UserEnum.get_from_id(user_id)
        if user is None:
            user_permission = RoleEnum.PLEB
        else:
            user_permission = user.permission_level
        if user_id in special_permissions:
            user_permission = RoleEnum.RESTRICTED
        role_access = RoleEnum.get_available_levels(user_permission)
        if RoleEnum.ADMIN in role_access or RoleEnum.DEVELOPER in role_access or RoleEnum.MEGUS in role_access:
            user_permission = user.permission_level
        available_commands_for_role = CommandsEnum.get_commands_of_specific_role(user_permission)
        return command in available_commands_for_role

    def is_allowed_to_mention(self, user_id, fuck_off):
        return (self.is_megus(user_id) or self.is_melon(user_id)) and fuck_off

    @staticmethod
    def is_channel_allowed(channel_name):
        return channel_name == "stoopids"

    @staticmethod
    def is_giannakis(id: int) -> bool:
        return UserEnum.is_giannakis(id)

    @staticmethod
    def is_megus(id: int) -> bool:
        return UserEnum.is_megus(id)

    @staticmethod
    def is_melon(id: int) -> bool:
        return UserEnum.is_melon(id)

    @staticmethod
    def is_bonko(id: int) -> bool:
        return UserEnum.is_bonko(id)

    @staticmethod
    def is_good_person(id: int) -> bool:
        return UserEnum.is_good_person(id)

from dataclasses import dataclass
from enum import Enum


class PermissionsEnum(Enum):
    DEVELOPER = "developer"

    ADMIN = "admin"

    RESTRICTED = "restricted"

    PUBLIC = "public"

    @staticmethod
    def get_available_levels(permission_level):
        if PermissionsEnum.is_developer_role(permission_level):
            return PermissionsEnum.get_developer_role_available_levels()
        if PermissionsEnum.is_admin_role(permission_level):
            return PermissionsEnum.get_admin_role_available_levels()
        if PermissionsEnum.is_restricted_role(permission_level):
            return PermissionsEnum.get_restricted_role_available_levels()
        if PermissionsEnum.is_public_role(permission_level):
            return PermissionsEnum.get_public_role_available_levels()

    @staticmethod
    def get_developer_role_available_levels():
        return [PermissionsEnum.DEVELOPER] + PermissionsEnum.get_admin_role_available_levels()

    @staticmethod
    def get_admin_role_available_levels():
        return [PermissionsEnum.ADMIN] + PermissionsEnum.get_restricted_role_available_levels()

    @staticmethod
    def get_restricted_role_available_levels():
        return [PermissionsEnum.RESTRICTED] + PermissionsEnum.get_public_role_available_levels()

    @staticmethod
    def get_public_role_available_levels():
        return [PermissionsEnum.PUBLIC]

    @staticmethod
    def is_allowed_to_use(role):
        return True

    @staticmethod
    def is_developer_role(role):
        return role == PermissionsEnum.DEVELOPER

    @staticmethod
    def is_admin_role(role):
        return role == PermissionsEnum.ADMIN

    @staticmethod
    def is_restricted_role(role):
        return role == PermissionsEnum.RESTRICTED

    @staticmethod
    def is_public_role(role):
        return role == PermissionsEnum.PUBLIC

    @staticmethod
    def get_from_string(role):
        for enum in PermissionsEnum:
            if enum.value.lower() == role.lower():
                return enum
        return None

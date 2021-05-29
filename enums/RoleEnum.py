from dataclasses import dataclass
from enum import Enum


class RoleEnum(Enum):
    MEGUS = "megus"

    DEVELOPER = "developer"

    ADMIN = "admin"

    RESTRICTED = "restricted"

    PUBLIC = "public"

    @staticmethod
    def get_available_levels(role):
        if RoleEnum.is_megus_role(role):
            return RoleEnum.get_megus_role_available_levels()
        if RoleEnum.is_developer_role(role):
            return RoleEnum.get_developer_role_available_levels()
        if RoleEnum.is_admin_role(role):
            return RoleEnum.get_admin_role_available_levels()
        if RoleEnum.is_restricted_role(role):
            return RoleEnum.get_restricted_role_available_levels()
        if RoleEnum.is_public_role(role):
            return RoleEnum.get_public_role_available_levels()

    @staticmethod
    def get_megus_role_available_levels():
        return [RoleEnum.MEGUS] + RoleEnum.get_developer_role_available_levels()

    @staticmethod
    def get_developer_role_available_levels():
        return [RoleEnum.DEVELOPER] + RoleEnum.get_admin_role_available_levels()

    @staticmethod
    def get_admin_role_available_levels():
        return [RoleEnum.ADMIN] + RoleEnum.get_restricted_role_available_levels()

    @staticmethod
    def get_restricted_role_available_levels():
        return [RoleEnum.RESTRICTED] + RoleEnum.get_public_role_available_levels()

    @staticmethod
    def get_public_role_available_levels():
        return [RoleEnum.PUBLIC]

    @staticmethod
    def is_allowed_to_use(role):
        return True

    @staticmethod
    def is_megus_role(role):
        return role == RoleEnum.MEGUS

    @staticmethod
    def is_developer_role(role):
        return role == RoleEnum.DEVELOPER

    @staticmethod
    def is_admin_role(role):
        return role == RoleEnum.ADMIN

    @staticmethod
    def is_restricted_role(role):
        return role == RoleEnum.RESTRICTED

    @staticmethod
    def is_public_role(role):
        return role == RoleEnum.PUBLIC

    @staticmethod
    def get_from_string(role):
        for role_enum in RoleEnum:
            if role_enum.value.lower() == role.lower():
                return role_enum
        return None

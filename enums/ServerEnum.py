from enum import Enum

from beans.Server import Server


class ServerEnum(Enum):
    GUYS = Server(443518313977479179, "guys")

    TEST = Server(842352768223936513, "test")

    @staticmethod
    def get_from_name(name):
        for enum in ServerEnum:
            if enum.value.name.lower() == name.lower():
                return enum
        return None

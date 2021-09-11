from enum import Enum

from beans.OnOff import OnOff


class OnOffEnum(Enum):
    NONE = OnOff(0, None)

    ON = OnOff(1, "on")

    OFF = OnOff(2, "off")

    @staticmethod
    def is_on(onOffEnum):
        return onOffEnum.value.id == OnOffEnum.ON.value.id

    @staticmethod
    def is_off(onOffEnum):
        return onOffEnum.value.id == OnOffEnum.OFF.value.id

    @staticmethod
    def is_none(onOffEnum):
        return onOffEnum.value.id == OnOffEnum.NONE.value.id

    @staticmethod
    def get_from_display(display):
        if display is None:
            return OnOffEnum.NONE
        for enum in OnOffEnum:
            enum_display = enum.value.display
            if enum_display and enum_display.lower() == display.lower():
                return enum
        return OnOffEnum.NONE

from enum import Enum


class DateFormatEnum(Enum):
    DATE_TIME = "%d/%m/%Y - %H:%M"

    YEAR = "%Y"

    @staticmethod
    def format_date_with_enum(timestamp, date_format_enum):
        return timestamp.strftime(date_format_enum.value)

    @staticmethod
    def format_date(timestamp, date_format):
        return timestamp.strftime(date_format)

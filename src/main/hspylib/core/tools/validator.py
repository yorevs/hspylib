import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Type, Callable


class Validator(ABC, Callable):

    class RegexCommons:
        PHONE_NUMBER = '((\\d{2})?\\s)?(\\d{4,5}\\-\\d{4})'
        COMMON_3_30_NAME = '[a-zA-Z]\\w{2,30}'
        EMAIL_W3C = '^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$'
        URL = '^(?:http(s)?:\\/\\/)?[\\w.-]+(?:\\.[\\w\\.-]+)+[\\w\\-\\._~:/?#[\\]@!\\$&\'\\(\\)\\*\\+,;=.]+$'

    @staticmethod
    def is_not_blank(input_string: str) -> bool:
        return input_string and len(input_string) > 0

    @staticmethod
    def matches(
            input_string: str,
            regex_pattern: str) -> bool:

        return bool(re.match(regex_pattern, input_string))

    @staticmethod
    def is_integer(
            number: str,
            min_value: int = 0,
            max_value: int = 65535) -> bool:

        return number.isdigit() and min_value <= int(number) <= max_value

    @staticmethod
    def is_float(
            number: str,
            min_value: float = 0,
            max_value: float = 65535) -> bool:

        return number.isdecimal() and min_value <= float(number) <= max_value

    @staticmethod
    def is_enum(
            name: str,
            enum_type: Type) -> bool:

        return name.upper() in enum_type.__dict__

    @staticmethod
    def is_date(
            date_text: str,
            fmt: str) -> bool:

        try:
            datetime.strptime(date_text, fmt)
            return True
        except ValueError:
            return False

    @abstractmethod
    def __call__(self, *args, **kwargs) -> bool:
        pass

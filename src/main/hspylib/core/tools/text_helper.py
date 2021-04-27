import random
import re

from hspylib.core.tools.commons import get_or_default


def fit_text(text: str, width: int) -> str:
    return text if len(text) <= width else text[0:width-3] + '...'


def rand_string(choices: str, length: int) -> str:
    return ''.join(random.choices(choices, k=length))


class TextHelper:
    @staticmethod
    def justified_left(string: str, width: int, fill: str = ' ') -> str:
        return string.ljust(width, fill)

    @staticmethod
    def justified_center(string: str, width: int, fill: str = ' ') -> str:
        return string.center(width, fill)

    @staticmethod
    def justified_right(string: str, width: int, fill: str = ' ') -> str:
        return string.rjust(width, fill)

    @staticmethod
    def uppercase(string: str) -> str:
        return string.upper()

    @staticmethod
    def lowercase(string: str) -> str:
        return string.lower()

    @staticmethod
    def camelcase(string: str) -> str:
        return string.capitalize()

    @staticmethod
    def cut(string: str, index: int) -> str:
        result = tuple(re.split(r' +', string))
        return get_or_default(result, index)


class TextAlignment:
    """
    Table cell text justification helper.
    """
    LEFT = TextHelper.justified_left
    CENTER = TextHelper.justified_center
    RIGHT = TextHelper.justified_right


class TextCase:
    """
    Table cell text justification helper.
    """
    UPPER_CASE = TextHelper.uppercase
    LOWER_CASE = TextHelper.lowercase
    CAMEL_CASE = TextHelper.camelcase

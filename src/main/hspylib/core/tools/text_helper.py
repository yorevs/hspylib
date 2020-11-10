from typing import Callable


class TextStyle:
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


class TextAlignment(Callable):
    """
    Table cell text justification helper.
    """
    LEFT = TextStyle.justified_left
    CENTER = TextStyle.justified_center
    RIGHT = TextStyle.justified_right


class TextCase(Callable):
    """
    Table cell text justification helper.
    """
    UPPER_CASE = TextStyle.uppercase
    LOWER_CASE = TextStyle.lowercase
    CAMEL_CASE = TextStyle.camelcase

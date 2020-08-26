class TextJustify:
    @staticmethod
    def justify_left(string: str, width: int, fill: str = ' ') -> str:
        return string.ljust(width, fill)

    @staticmethod
    def justify_center(string: str, width: int, fill: str = ' ') -> str:
        return string.center(width, fill)

    @staticmethod
    def justify_right(string: str, width: int, fill: str = ' ') -> str:
        return string.rjust(width, fill)

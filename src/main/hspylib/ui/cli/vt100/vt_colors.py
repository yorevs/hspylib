from enum import Enum

ESC = '\033'
SEQ = '['
ESC_SEQ = ESC + SEQ

# Esc[<FormatCode>m
MODE = 'm'


class VtColors(Enum):
    NC = '{}0;0;0{}'.format(ESC_SEQ, MODE)
    BLACK = '{}0;30{}'.format(ESC_SEQ, MODE)
    RED = '{}0;31{}'.format(ESC_SEQ, MODE)
    GREEN = '{}0;32{}'.format(ESC_SEQ, MODE)
    YELLOW = '{}0;93{}'.format(ESC_SEQ, MODE)
    BLUE = '{}0;34{}'.format(ESC_SEQ, MODE)
    PURPLE = '{}35{}'.format(ESC_SEQ, MODE)
    CYAN = '{}36{}'.format(ESC_SEQ, MODE)
    GRAY = '{}38;5;8{}'.format(ESC_SEQ, MODE)
    ORANGE = '{}38;5;202{}'.format(ESC_SEQ, MODE)
    VIOLET = '{}0;95{}'.format(ESC_SEQ, MODE)
    WHITE = '{}0;97{}'.format(ESC_SEQ, MODE)

    @staticmethod
    def colorize(input_string: str):
        return input_string \
               .replace("%NC%", VtColors.NC.code()) \
               .replace("%BLACK%", VtColors.BLACK.code()) \
               .replace("%RED%", VtColors.RED.code()) \
               .replace("%GREEN%", VtColors.GREEN.code()) \
               .replace("%YELLOW%", VtColors.YELLOW.code()) \
               .replace("%BLUE%", VtColors.BLUE.code()) \
               .replace("%PURPLE%", VtColors.PURPLE.code()) \
               .replace("%CYAN%", VtColors.CYAN.code()) \
               .replace("%GRAY%", VtColors.GRAY.code()) \
               .replace("%ORANGE%", VtColors.ORANGE.code()) \
               .replace("%VIOLET%", VtColors.VIOLET.code()) \
               .replace("%WHITE%", VtColors.WHITE.code()) \
               + VtColors.NC.code()

    def __str__(self):
        return self._value_

    def code(self) -> str:
        return str(self)

import re
from enum import Enum, auto

from hspylib.ui.cli.vt100.vt_100 import Vt100

# For all mnemonics that take arguments we need to include in this map
VT100_FNC_MAP = {
    "CUP": Vt100.cursor_pos,
    "CUU": Vt100.cursor_move_up,
    "CUD": Vt100.cursor_move_down,
    "CUF": Vt100.cursor_move_forward,
    "CUB": Vt100.cursor_move_backward,
    "MOD": Vt100.mode,
}


def vt_print(vt100_str: str) -> None:
    print(VtCodes.decode(vt100_str), end='')


class VtCodes(Enum):
    # VT-100 mnemonics
    CSV = Vt100.save_cursor()           # ^[7
    CRE = Vt100.restore_cursor()        # ^[8
    SAW = Vt100.set_auto_wrap(True)     # ^[?7h
    UAW = Vt100.set_auto_wrap(False)    # ^[?7l
    SSC = Vt100.set_show_cursor(True)   # ^[?25h
    USC = Vt100.set_show_cursor(False)  # ^[?25l

    ED0 = Vt100.clear_screen()    # ^[[J
    ED1 = Vt100.clear_screen(1)   # ^[[1J
    ED2 = Vt100.clear_screen(2)   # ^[[2J
    EL0 = Vt100.clear_line()      # ^[[K
    EL1 = Vt100.clear_line(1)     # ^[[1K
    EL2 = Vt100.clear_line(2)     # ^[[2K
    HOM = Vt100.cursor_pos()      # ^[[H
    CUP = auto()                  # ^[[<v>;<h>H
    CUU = auto()                  # ^[[<n>A
    CUD = auto()                  # ^[[<n>B
    CUF = auto()                  # ^[[<n>C
    CUB = auto()                  # ^[[<n>D
    MOD = auto()                  # ^[[<m1;m2;m3>m

    @staticmethod
    def decode(input_string: str) -> str:
        results = re.findall(r'%VT_([a-zA-Z0-9]+)(\([0-9]+(;[0-9]+)*\))?%', input_string)
        for nextResult in results:
            mnemonic = str(nextResult[0])
            args = nextResult[1][1:-1] if nextResult[1] else ''
            if args:
                input_string = input_string.replace(
                    '%VT_{}%'.format(mnemonic + nextResult[1]), VtCodes[mnemonic](args))
            else:
                input_string = input_string.replace(
                    '%VT_{}%'.format(mnemonic), VtCodes[mnemonic].value)

        return input_string

    def __call__(self, *args, **kwargs) -> str:
        return VT100_FNC_MAP[self.name](args[0])

    def __str__(self) -> str:
        return self._value_

    def code(self) -> str:
        return str(self)

    def placeholder(self) -> str:
        return '%{}%'.format(self.name)

import re
from enum import auto

from hspylib.core.enum.enumeration import Enumeration

from hspylib.ui.cli.vt100.vt_100 import Vt100


def vt_print(vt100_str: str) -> None:
    print(VtCodes.decode(vt100_str), end='')


class VtCodes(Enumeration):
    """VT-100 escape codes"""
    CSV = Vt100.save_cursor()           # ^[7
    CRE = Vt100.restore_cursor()        # ^[8

    SAW = Vt100.set_auto_wrap(True)     # ^[?7h
    UAW = Vt100.set_auto_wrap(False)    # ^[?7l
    SSC = Vt100.set_show_cursor(True)   # ^[?25h
    USC = Vt100.set_show_cursor(False)  # ^[?25l

    ED0 = Vt100.clear_screen()   # ^[[J
    ED1 = Vt100.clear_screen(1)  # ^[[1J
    ED2 = Vt100.clear_screen(2)  # ^[[2J
    EL0 = Vt100.clear_line()     # ^[[K
    EL1 = Vt100.clear_line(1)    # ^[[1K
    EL2 = Vt100.clear_line(2)    # ^[[2K
    HOM = Vt100.cursor_pos()     # ^[[H

    CUP = auto()  # ^[[<v>;<h>H
    CUU = auto()  # ^[[<n>A
    CUD = auto()  # ^[[<n>B
    CUF = auto()  # ^[[<n>C
    CUB = auto()  # ^[[<n>D
    MOD = auto()  # ^[[<m1;m2;m3>m

    # For all mnemonics that take arguments we need to include in this map
    __VT100_FNC_MAP__ = {
        "CUP": Vt100.cursor_pos,
        "CUU": Vt100.cursor_move_up,
        "CUD": Vt100.cursor_move_down,
        "CUF": Vt100.cursor_move_forward,
        "CUB": Vt100.cursor_move_backward,
        "MOD": Vt100.mode,
    }

    @classmethod
    def decode(cls, input_string: str) -> str:
        results = re.findall(r'%([a-zA-Z0-9]+)(\([0-9]+(;[0-9]+)*\))?%', input_string)
        for nextResult in results:
            mnemonic = nextResult[0]
            if mnemonic in VtCodes.names():
                args = nextResult[1][1:-1] if nextResult[1] else ''
                if args:
                    input_string = input_string.replace(
                        '%{}%'.format(mnemonic + nextResult[1]), VtCodes.value_of(mnemonic)(args))
                else:
                    input_string = input_string.replace(
                        '%{}%'.format(mnemonic), VtCodes.value_of(mnemonic).value)

        return input_string

    def __call__(self, *args, **kwargs) -> str:
        return VtCodes.__VT100_FNC_MAP__[self.name](args[0])

    def __str__(self) -> str:
        return self._value_

    def code(self) -> str:
        return str(self)

    def placeholder(self) -> str:
        return f"%{self.name}%"

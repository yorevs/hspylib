#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.vt100
      @file: vt_codes.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
from enum import auto

from hspylib.core.enums.enumeration import Enumeration
from hspylib.modules.cli.vt100.vt_100 import Vt100


def vt_print(vt100_str: str, end: str = '') -> None:
    """Print a vt-100 encoded string. VT-100 string will contain one or more %VT-100-CODE% """
    print(VtCodes.decode(vt100_str), end=end)


class VtCodes(Enumeration):
    """VT-100 escape codes"""

    # @formatter:off
    CSV = Vt100.save_cursor()           # ^[7 -> Save cursor position and attributes
    CRE = Vt100.restore_cursor()        # ^[8 -> Restore cursor position and attributes
    RIS = Vt100.reset()                 # ^[c -> Reset terminal to initial state

    SAW = Vt100.set_auto_wrap(True)     # ^[?7h  -> Set auto-wrap mode
    UAW = Vt100.set_auto_wrap(False)    # ^[?7l  -> Unset auto-wrap mode
    SSC = Vt100.set_show_cursor(True)   # ^[?25h -> Set show cursor
    USC = Vt100.set_show_cursor(False)  # ^[?25l -> Unset show cursor

    ED0 = Vt100.clear_screen()          # ^[[J  -> Clear screen from cursor down
    ED1 = Vt100.clear_screen(1)         # ^[[1J -> Clear screen from cursor up
    ED2 = Vt100.clear_screen(2)         # ^[[2J -> Clear entire screen

    EL0 = Vt100.clear_line()            # ^[[K  -> Clear line from cursor right
    EL1 = Vt100.clear_line(1)           # ^[[1K -> Clear line from cursor left
    EL2 = Vt100.clear_line(2)           # ^[[2K -> Clear entire line

    HOM = Vt100.cursor_pos()            # ^[[H  -> Move cursor to upper left corner

    # The following entries must defined as auto(), so they can be invoked as Callable

    MOD = auto()                        # ^[[<m1;m2;m3>m  -> Set terminal modes
    CUP = auto()                        # ^[[<v>;<h>H     -> Move cursor to screen location <v,h>
    CUU = auto()                        # ^[[<n>A         -> Move cursor up n lines
    CUD = auto()                        # ^[[<n>B         -> Move cursor down n lines
    CUF = auto()                        # ^[[<n>C         -> Move cursor right n lines
    CUB = auto()                        # ^[[<n>D         -> Move cursor left n lines
    # @formatter:on

    # For all mnemonics that take arguments we need to include in this map, so we can call it
    __VT100_FNC_MAP__ = {
        "MOD": Vt100.mode,
        "CUP": Vt100.cursor_pos,
        "CUU": Vt100.cursor_move_up,
        "CUD": Vt100.cursor_move_down,
        "CUF": Vt100.cursor_move_forward,
        "CUB": Vt100.cursor_move_backward,
    }

    @classmethod
    def decode(cls, input_string: str) -> str:
        """Decode the string into a VT_CODE enum"""
        results = re.findall(r'%([a-zA-Z0-9]+)(\([0-9]+(;[0-9]+)*\))?%', input_string)
        for nextResult in results:
            mnemonic = nextResult[0]
            if mnemonic in VtCodes.names():
                args = nextResult[1][1:-1] if nextResult[1] else ''
                if args:
                    input_string = input_string.replace(
                        f'%{mnemonic + nextResult[1]}%', VtCodes.value_of(mnemonic)(args))
                else:
                    input_string = input_string.replace(
                        f'%{mnemonic}%', VtCodes.value_of(mnemonic).value)

        return input_string

    def __call__(self, *args, **kwargs) -> str:
        return VtCodes.__VT100_FNC_MAP__[self.name](args[0])

    def __str__(self) -> str:
        return str(self.value)

    def code(self) -> str:
        """Decode the string into a VT_CODE enum"""
        return str(self)

    def placeholder(self) -> str:
        """Decode the string into a VT_CODE enum"""
        return f"%{self.name}%"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.vt100
      @file: vt_codes.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
import re
from typing import Callable, Optional

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.preconditions import check_state
from hspylib.modules.cli.vt100.vt_100 import Vt100


class VtCode(Enumeration):
    """VT-100 escape codes
    Ref.: http://domoticx.com/terminal-codes-ansivt100/
    """

    # fmt: off

    CSV = Vt100.save_cursor()               # ^[7 -> Save cursor position and attributes
    CRE = Vt100.restore_cursor()            # ^[8 -> Restore cursor position and attributes
    RIS = Vt100.reset()                     # ^[c -> Reset terminal to initial state

    SAW = Vt100.set_auto_wrap(True)         # ^[?7h  -> Set auto-wrap mode
    UAW = Vt100.set_auto_wrap(False)        # ^[?7l  -> Unset auto-wrap mode
    SSC = Vt100.set_show_cursor(True)       # ^[?25h -> Set show cursor
    USC = Vt100.set_show_cursor(False)      # ^[?25l -> Unset show cursor

    ED0 = Vt100.clear_screen()              # ^[[J  -> Clear screen from cursor down
    ED1 = Vt100.clear_screen(1)             # ^[[1J -> Clear screen from cursor up
    ED2 = Vt100.clear_screen(2)             # ^[[2J -> Clear entire screen

    EL0 = Vt100.clear_line()                # ^[[K  -> Clear line from cursor right
    EL1 = Vt100.clear_line(1)               # ^[[1K -> Clear line from cursor left
    EL2 = Vt100.clear_line(2)               # ^[[2K -> Clear entire line

    HOM = Vt100.set_cursor_pos()            # ^[[H  -> Move cursor to upper left corner

    SCA = Vt100.alternate_screen()          # ^[?1049h -> Switch to alternate screen buffer
    SCM = Vt100.alternate_screen(False)     # ^[?1049l -> Switch to main screen buffer

    EOL = os.linesep                        # Line separator (eol)

    # For all commands that take arguments, we need to add to this map, so we can call it.
    # The following entry values must defined as auto(), so they can be invoked as Callable

    MOD = "MOD"  # ^[[<m1;m2;m3>m  -> Set terminal modes
    CUP = "CUP"  # ^[[<v>;<h>H     -> Move cursor to screen location <v,h>
    CUU = "CUU"  # ^[[<n>A         -> Move cursor up n lines
    CUD = "CUD"  # ^[[<n>B         -> Move cursor down n lines
    CUF = "CUF"  # ^[[<n>C         -> Move cursor right n lines
    CUB = "CUB"  # ^[[<n>D         -> Move cursor left n lines

    # fmt: on

    @staticmethod
    def _vt100_fnc(command: str) -> Optional[Callable]:
        """Return the corresponding VT100 function specified by command."""
        fnc = None
        match command:
            case "MOD":
                fnc = Vt100.mode
            case "CUP":
                fnc = Vt100.set_cursor_pos
            case "CUU":
                fnc = Vt100.cursor_move_up
            case "CUD":
                fnc = Vt100.cursor_move_down
            case "CUF":
                fnc = Vt100.cursor_move_forward
            case "CUB":
                fnc = Vt100.cursor_move_backward
        return fnc

    @classmethod
    def decode(cls, input_string: str) -> str:
        """Decode the string into a VT_CODE enum."""
        commands = re.findall(r"%([a-zA-Z0-9]+)(\([0-9]+(;[0-9]+)*\))?%", input_string)
        for cmd in commands:
            if (mnemonic := cmd[0]) in VtCode.names():
                args = cmd[1][1:-1] if cmd[1] else None
                if args:  # If has args we need to invoke the vt100 function
                    if fnc := VtCode.value_of(mnemonic).__call__:
                        input_string = input_string \
                            .replace(f"%{mnemonic + cmd[1]}%", fnc(args) if fnc else "")
                else:
                    input_string = input_string \
                        .replace(f"%{mnemonic}%", str(VtCode.value_of(mnemonic).value))

        return input_string

    def __call__(self, *args, **kwargs) -> str:
        fn = VtCode._vt100_fnc(self.name)
        check_state(fn and callable(fn), f"Could not find a proper function for {self.name}")
        return fn(*args)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def code(self) -> str:
        """Decode the string into a VT_CODE enum"""
        return str(self)

    @property
    def placeholder(self) -> str:
        """Decode the string into a VT_CODE enum"""
        return f"%{self.name}%"

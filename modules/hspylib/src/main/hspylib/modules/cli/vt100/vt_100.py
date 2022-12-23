#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.vt100
      @file: vt_100.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
import re
from abc import ABC

from hspylib.core.preconditions import check_argument


class Vt100(ABC):
    """
    References:
        - https://vt100.net/docs/vt100-ug/chapter3.html
        - https://espterm.github.io/docs/VT100%20escape%20codes.html
    """

    TERM = os.environ.get('TERM', 'xterm-color')

    # Esc<Sequence>
    @staticmethod
    def escape(seq: str) -> str:
        """TODO"""
        return f"\033{seq}"

    # Esc[<Code>
    @staticmethod
    def sequence(code: str) -> str:
        """TODO"""
        return Vt100.escape(f"[{code}")

    # Esc7
    @staticmethod
    def save_cursor() -> str:
        """TODO"""
        return Vt100.escape("7")

    # Esc8
    @staticmethod
    def restore_cursor() -> str:
        """TODO"""
        return Vt100.escape("8")

    # Esc[c
    @staticmethod
    def reset() -> str:
        """TODO"""
        return Vt100.sequence("c")

    # Esc[?7<h/l>
    @staticmethod
    def set_auto_wrap(enabled: bool) -> str:
        """TODO"""
        return Vt100.sequence(f"?7{'h' if enabled else 'l'}")

    # Esc[?25<h/l>
    @staticmethod
    def set_show_cursor(enabled: bool) -> str:
        """TODO"""
        return Vt100.sequence(f"?25{'h' if enabled else 'l'}")

    # Esc[?25<h/l>
    @staticmethod
    def get_cursor_pos() -> str:
        """TODO"""
        return Vt100.sequence("6n")

    # Esc[<Modes...>m
    @staticmethod
    def mode(mod_seq: str) -> str:
        """TODO"""
        check_argument(bool(re.match(r"[0-9]+(;[0-9]+){0,2}", mod_seq)), f"Invalid mode sequence: {mod_seq}")
        return Vt100.sequence(f"{mod_seq}m")

    # Esc[<n>J
    @staticmethod
    def clear_screen(mod_cls: int = None) -> str:
        """TODO"""
        if not mod_cls:
            return Vt100.sequence("J")
        check_argument(mod_cls in [0, 1, 2], f"Invalid clear screen sequence: {mod_cls}")
        return Vt100.sequence(f"{mod_cls}J")

    # Esc[<n>K
    @staticmethod
    def clear_line(mod_cls: int = None) -> str:
        """TODO"""
        if not mod_cls:
            return Vt100.sequence("K")
        check_argument(mod_cls in [0, 1, 2], f"Invalid clea line sequence: {mod_cls}")
        return Vt100.sequence(f"{mod_cls}K")

    # Esc[<v>;<h>H
    @staticmethod
    def set_cursor_pos(cup_seq: str = None) -> str:
        """TODO"""
        if not cup_seq:
            return Vt100.sequence("H")
        check_argument(bool(re.match(r"[0-9]*;[0-9]*", cup_seq)), f"Invalid cursor position sequence: {cup_seq}")
        return Vt100.sequence(f"{cup_seq}H")

    # Esc[<n><A/B/C/D>
    @staticmethod
    def cursor_move(amount: int, direction: str) -> str:
        """TODO"""
        check_argument(
            int(amount) >= 0 and direction in ["A", "B", "C", "D"],
            f"Invalid direction={direction} or move amount={amount}",
        )
        return Vt100.sequence(f"{amount}{direction}")

    # Esc[<n>A
    @staticmethod
    def cursor_move_up(amount: int = None) -> str:
        """TODO"""
        return Vt100.cursor_move(amount or 0, "A")

    # Esc[<n>B
    @staticmethod
    def cursor_move_down(amount: int = None) -> str:
        """TODO"""
        return Vt100.cursor_move(amount or 0, "B")

    # Esc[<n>C
    @staticmethod
    def cursor_move_forward(amount: int = None) -> str:
        """TODO"""
        return Vt100.cursor_move(amount or 0, "C")

    # Esc[<n>D
    @staticmethod
    def cursor_move_backward(amount: int = None) -> str:
        """TODO"""
        return Vt100.cursor_move(amount or 0, "D")

    # Esc[?1049<h/l>
    @staticmethod
    def alternate_screen(enable: bool = True) -> str:
        """TODO"""
        match Vt100.TERM:
            case "xterm-256color":
                return Vt100.sequence(f"?1049{'h' if enable else 'l'}")
            case "xterm-color":
                if enable:
                    return Vt100.escape("7") + Vt100.sequence("?47h")
                return Vt100.sequence("2J") + Vt100.sequence("?47l") + Vt100.escape("8")
            case _:
                return NotImplemented

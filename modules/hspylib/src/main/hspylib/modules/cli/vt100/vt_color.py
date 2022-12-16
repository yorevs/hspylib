#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.vt100
      @file: vt_colors.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from enum import auto

from hspylib.core.enums.enumeration import Enumeration
from hspylib.modules.cli.vt100.vt_100 import Vt100


# pylint: disable=multiple-statements
# @composable
class VtColor(Enumeration):
    """
    Ref.: https://en.wikipedia.org/wiki/ANSI_escape_code#SGR
    """

    # fmt: off
    _CUSTOM = auto()
    NC      = Vt100.mode('0;0;0')       ; BLACK   = Vt100.mode('30')
    RED     = Vt100.mode('31')          ; BG_RED     = Vt100.mode('41')
    GREEN   = Vt100.mode('32')          ; BG_GREEN   = Vt100.mode('42')
    YELLOW  = Vt100.mode('93')          ; BG_YELLOW  = Vt100.mode('43')
    BLUE    = Vt100.mode('34')          ; BG_BLUE    = Vt100.mode('44')
    PURPLE  = Vt100.mode('35')          ; BG_PURPLE  = Vt100.mode('45')
    CYAN    = Vt100.mode('36')          ; BG_CYAN    = Vt100.mode('46')
    GRAY    = Vt100.mode('38;5;8')      ; BG_GRAY    = Vt100.mode('47')
    ORANGE  = Vt100.mode('38;5;202')    ; BG_ORANGE  = Vt100.mode('48;5;202')
    VIOLET  = Vt100.mode('95')          ; BG_VIOLET  = Vt100.mode('48;5;90')
    WHITE   = Vt100.mode('97')          ; BG_WHITE   = Vt100.mode('48;5;255')
    # fmt: on

    @classmethod
    def colorize(cls, input_string: str) -> str:
        colorized = input_string
        for color in cls.names():
            colorized = cls._replace_all(colorized, color)
        return colorized

    @classmethod
    def strip_colors(cls, input_string: str) -> str:
        plain = input_string
        for color in cls.names():
            plain = plain.replace(f"%{color}%", "")
        return plain

    @classmethod
    def _replace_all(cls, input_string: str, color_name: str) -> str:
        color = VtColor.value_of(color_name.upper())
        return input_string.replace(color.placeholder, color.code)

    @property
    def code(self) -> str:
        return str(self.value)

    @property
    def placeholder(self) -> str:
        return f"%{self.name}%"

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

   Copyright 2021, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration
from hspylib.modules.cli.vt100.vt_100 import Vt100


class VtColors(Enumeration):
    """TODO"""

    NC = Vt100.mode('0;0;0')
    BLACK = Vt100.mode('0;30')
    RED = Vt100.mode('0;31')
    GREEN = Vt100.mode('0;32')
    YELLOW = Vt100.mode('0;93')
    BLUE = Vt100.mode('0;34')
    PURPLE = Vt100.mode('35')
    CYAN = Vt100.mode('36')
    GRAY = Vt100.mode('38;5;8')
    ORANGE = Vt100.mode('38;5;202')
    VIOLET = Vt100.mode('0;95')
    WHITE = Vt100.mode('0;97')

    @staticmethod
    def colorize(input_string: str) -> str:
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
            .replace("%WHITE%", VtColors.WHITE.code())

    def code(self) -> str:
        return str(self)

    def placeholder(self) -> str:
        return f"%{self.name}%"

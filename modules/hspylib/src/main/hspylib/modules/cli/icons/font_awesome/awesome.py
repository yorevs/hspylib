#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.icons.font_awesome
      @file: awesome.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import re
import struct
from typing import TypeVar, Union

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import eol

AwesomeClass = TypeVar('AwesomeClass')


class Awesome(Enumeration):
    """
    Font awesome codes
    Full list of font awesome icons can be found here:
      - https://fontawesome.com/cheatsheet?from=io
    """

    @staticmethod
    def compose(*icons: "Awesome") -> str:
        result = ""
        for i in icons:
            result += i.unicode
        return result

    @staticmethod
    def print_unicode(uni_code: Union[str, int], end: str = "") -> None:
        """TODO"""
        if isinstance(uni_code, str) and re.match(r"^[a-fA-F0-9]{1,4}$", uni_code):
            hex_val = bytes.decode(struct.pack("!I", int(uni_code.zfill(4), 16)), "utf_32_be")
            sysout(f"{hex_val:2s}", end=end)
        elif isinstance(uni_code, int):
            hex_val = bytes.decode(struct.pack("!I", uni_code), "utf_32_be")
            sysout(f"{hex_val:2s}", end=end)
        else:
            raise TypeError(f"Invalid unicode value: {uni_code}")

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    @property
    def unicode(self) -> str:
        return str(self.value)


def demo_unicodes(split_columns: int = 16, fa_start: int = 0xF000, fa_end: int = 0xFD50) -> None:
    """TODO"""
    fa_range = fa_start, fa_end  # Font awesome range unicodes
    st_base = [f"{hex(x)[2:]}" for x in range(*fa_range)]
    for n, h in enumerate(st_base):
        Awesome.print_unicode(h)
        sysout(f"{h:04}", end=eol(n, split_columns))


def demo_icons(split_columns: int = 16, awesome: AwesomeClass = Awesome) -> None:
    """TODO"""
    for i, n in enumerate(awesome.values()):
        sysout(f"{n:2}", end=eol(i, split_columns))

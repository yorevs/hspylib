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
from typing import Union
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import eol


class Awesome(Enumeration):
    """
        Font awesome codes
        Full list of font awesome icons can be found here:
          - https://fontawesome.com/cheatsheet?from=io
    """

    @staticmethod
    def print_unicode(uni_code: Union[str, int]) -> None:
        """TODO"""
        if isinstance(uni_code, str) and re.match(r"^[a-fA-F0-9]{1,4}$", uni_code):
            hex_val = bytes.decode(struct.pack("!I", int(uni_code.zfill(4), 16)), 'utf_32_be')
            sysout(hex_val, end='')
        elif isinstance(uni_code, int):
            hex_val = bytes.decode(struct.pack("!I", uni_code), 'utf_32_be')
            sysout(hex_val, end='')
        else:
            raise TypeError(f'Invalid unicode: {uni_code}')

    @staticmethod
    def demo_unicodes() -> None:
        """TODO"""
        n = 0
        st_base = [f'F{x:03X}' for x in range(0, 4095)]
        for h in st_base:
            Awesome.print_unicode(h)
            sysout(f' {h:4}', end=eol(n, 10))
            n += 1

    @classmethod
    def demo_icons(cls) -> None:
        """TODO"""
        i = 0
        for n in cls.values():
            sysout(f'{n:2}', end=eol(i, 10))
            i += 1

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self):
        return str(self)

    def placeholder(self) -> str:
        """TODO"""
        return f":{self.name}:"


if __name__ == '__main__':
    Awesome.demo_unicodes()

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

   Copyright 2021, HSPyLib team
"""

import struct

from core.enums.enumeration import Enumeration


class Awesome(Enumeration):
    """
        Font awesome codes
        Full list of font awesome icons can be found here:
          - https://fontawesome.com/cheatsheet?from=io
    """

    @staticmethod
    def demo_unicodes() -> None:
        i = 0
        st_base = [f'F{x:03X}' for x in range(0, 4095)]
        for n in st_base:
            hex_val = bytes.decode(struct.pack("!I", int(n, 16)), 'utf_32_be')
            end_line = '\n' if i != 0 and i % 10 == 0 else ' '
            print(f'{hex_val} {n:4}', end=end_line)
            i += 1

    @classmethod
    def demo_icons(cls) -> None:
        i = 0
        for n in cls.values():
            end_line = '\n' if i != 0 and i % 10 == 0 else ' '
            print(f'{n:2}', end=end_line)
            i += 1

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self):
        return str(self)

    def placeholder(self) -> str:
        return f":{self.name}:"


if __name__ == '__main__':
    Awesome.demo_unicodes()

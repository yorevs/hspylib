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

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import end_ln, print_unicode


class Awesome(Enumeration):
    """
        Font awesome codes
        Full list of font awesome icons can be found here:
          - https://fontawesome.com/cheatsheet?from=io
    """

    @staticmethod
    def demo_unicodes() -> None:
        n = 0
        st_base = [f'F{x:03X}' for x in range(0, 4095)]
        for h in st_base:
            print_unicode(h)
            sysout(f' {h:4}', end=end_ln(n, 10))
            n += 1

    @classmethod
    def demo_icons(cls) -> None:
        i = 0
        for n in cls.values():
            sysout(f'{n:2}', end=end_ln(n, 10))
            i += 1

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self):
        return str(self)

    def placeholder(self) -> str:
        return f":{self.name}:"


if __name__ == '__main__':
    Awesome.demo_unicodes()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.icons.font_awesome
      @file: awesome.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import struct

from idna.core import unicode

from hspylib.core.enums.enumeration import Enumeration


def awe_print(awesome_str: str) -> None:
    print(awesome_str + ' ', end='')


class Awesome(Enumeration):
    """
        Font awesome codes
        Full list of font awesome icons can be found here:
          - https://fontawesome.com/cheatsheet?from=io
    """
    
    @staticmethod
    def demo_unicode() -> None:
        i = 0
        st_base = ['F{:03X}'.format(x) for x in range(0, 4095)]
        for n in st_base:
            hexa = unicode(struct.pack("!I", int(n, 16)), 'utf_32_be')
            endz = '\n' if i != 0 and i % 10 == 0 else ' '
            print('{} {}'.format(hexa, n), end=endz)
            i += 1
    
    @classmethod
    def demo_icons(cls) -> None:
        list(map(awe_print, cls.values()))
    
    def __str__(self) -> str:
        return str(self.value)
    
    def placeholder(self) -> str:
        return f":{self.name}:"


if __name__ == '__main__':
    Awesome.demo_unicode()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.icons.font_awesome
      @file: awesome_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.awesome import Awesome
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import eol


def demo_unicodes(fa_start: int = 0xF000, fa_end: int = 0xFD50, split_columns: int = 16) -> None:
    """
     BoxDrawing: demo_unicodes(0x2500, 0x257F)
    FontAwesome: demo_unicodes(0xF000, 0xFD50)
    """
    fa_range = fa_start, fa_end  # Font awesome range unicodes
    st_base = [f"{hex(x)[2:]}" for x in range(*fa_range)]
    for n, h in enumerate(st_base):
        Awesome.print_unicode(h)
        sysout(f"{h.upper():04}", end=eol(n, split_columns))


if __name__ == "__main__":
    print("\n\nALL UNICODES " + "-" * 30)
    demo_unicodes()

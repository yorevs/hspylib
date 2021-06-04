#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.cli.tui.extra
      @file: menu_select.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from hspylib.modules.cli.tui.extra.mselect import mselect

if __name__ == '__main__':
    it = [f"Item-{n}" for n in range(1, 21)]
    sel = mselect(it, max_rows=10)
    print(str(sel))

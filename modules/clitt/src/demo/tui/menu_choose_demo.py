#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui
      @file: menu_choose_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.mchoose import mchoose
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.modules.cli.vt100.vt_color import VtColor


class ChooseableItem:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Name: {self.name} Value: {self.value}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    TUIPreferences(max_rows=10, highlight_color=VtColor.WHITE)
    quantity = 22
    digits = len(str(quantity))
    it = [ChooseableItem(f"Item-{n:>0{digits}}", f"Value-{n:>0{digits}}") for n in range(1, quantity)]
    sel = mchoose(it)
    print(str(sel))

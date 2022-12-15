#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.tui.components
      @file: menu_choose_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.cli.tui.mchoose import mchoose
from hspylib.modules.cli.tui.tui_preferences import TUIPreferences
from hspylib.modules.cli.vt100.vt_colors import VtColors


class ChooseableItem:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Name: {self.name} Value: {self.value}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    TUIPreferences(max_rows=10, highlight_color=VtColors.WHITE)
    quantity = 21
    it = [ChooseableItem(f"Item-{n}", f"Value-{n}") for n in range(1, quantity)]
    sel = mchoose(it)
    print(str(sel))

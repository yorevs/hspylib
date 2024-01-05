#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui
      @file: menu_select_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from clitt.core.tui.mselect.mselect import mselect


class SelectableItem:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Name: {self.name} Value: {self.value}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    quantity = 22
    digits = len(str(quantity))
    it = [SelectableItem(f"Item-{n:>0{digits}}", f"Value-{n:>0{digits}}") for n in range(1, quantity)]
    sel = mselect(it)
    print(str(sel))

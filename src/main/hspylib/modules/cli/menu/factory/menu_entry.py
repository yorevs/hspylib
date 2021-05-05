#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.factory
      @file: menu_entry.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.menu.menu import Menu
from hspylib.modules.cli.menu.menu_item import MenuItem
from hspylib.modules.cli.vt100.vt_colors import VtColors

MENU_TPL = """%ED2%%HOM%
{}

{}
"""


class MenuEntry(MenuItem):
    def __init__(self, parent: Menu, items: dict, title: str = None, color: VtColors = VtColors.ORANGE):
        super().__init__(parent, title)
        title_len = round(len(title) / 2) + 2
        self.menu_data = MENU_TPL.format(
            '{}{}\n  {}\n{}'.format(
                color.placeholder(),
                '-=' * title_len,
                self.title,
                '-=' * title_len),
            '\n'.join([str(value) for key, value in items.items()])
        )
        self.options = range(0, len(items))
        self.items = items
    
    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        ret_val = self.items[str(int_op)].action_trigger(self)
        
        return ret_val if ret_val else self

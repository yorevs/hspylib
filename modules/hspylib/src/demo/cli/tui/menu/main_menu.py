#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.tui
      @file: main_menu.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from cli.tui.menu.sub_menu_1 import SubMenu1
from cli.tui.menu.sub_menu_2 import SubMenu2
from hspylib.modules.cli.tui.menu.menu import Menu
from hspylib.modules.cli.tui.menu.menu_item import MenuItem
from hspylib.modules.cli.vt100.vt_utils import exit_app
MENU = """%ED2%%HOM%
{}

%GREEN%[0]%NC% Exit
%GREEN%[1]%NC% Sub Menu 1
%GREEN%[2]%NC% Sub Menu 2
"""


class MainMenu(MenuItem):
    def __init__(self):
        super().__init__(title='Static Main Menu')
        self.menu_data = str(MENU).format(self.title)
        self.options = range(0, 3)
        self.menu_items = {
            '1': SubMenu1(parent=self),
            '2': SubMenu2(parent=self)
        }

    def trigger_menu_item(self) -> Menu:  # pylint: disable=inconsistent-return-statements
        int_op = int(str(self.selected).strip())
        if int_op == 0:
            exit_app(0)
        else:
            return self.menu_items[str(int_op)]

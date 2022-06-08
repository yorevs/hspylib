#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.tui
      @file: sub_menu_2.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.cli.tui.menu.menu import Menu
from hspylib.modules.cli.tui.menu.menu_item import MenuItem

MENU = """%ED2%%HOM%
{}

%GREEN%[0]%NC% Back
%GREEN%[1]%NC% Print Hello
%GREEN%[2]%NC% Print Hi
"""


class SubMenu2(MenuItem):
    def __init__(self, parent: Menu = None):
        super().__init__(parent, '-= Sub Menu 2 =-')
        self.menu_data = str(MENU).format(self.title)
        self.options = range(0, 3)

    def trigger_menu_item(self) -> Menu:
        int_op = int(str(self.selected).strip())
        if int_op == 0:
            return self.parent

        if int_op == 1:
            print('Hello')
        elif int_op == 2:
            print('Hi')

        return self

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.cli.menu
      @file: main_menu.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from cli.menu.sub_menu_1 import SubMenu1
from cli.menu.sub_menu_2 import SubMenu2
from hspylib.modules.cli.menu.menu import Menu
from hspylib.modules.cli.menu.menu_item import MenuItem
from hspylib.modules.cli.menu.menu_utils import MenuUtils

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
            MenuUtils.exit_app(0)
        else:
            return self.menu_items[str(int_op)]

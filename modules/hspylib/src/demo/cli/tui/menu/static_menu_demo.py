#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.cli.tui
      @file: static_menu_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from hspylib.modules.cli.tui.menu.menu_ui import MenuUi

from cli.tui.menu.main_menu import MainMenu

if __name__ == '__main__':
    mm = MenuUi(MainMenu())
    mm.show()

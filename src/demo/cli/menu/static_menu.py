#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.cli.menu
      @file: static_menu.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from cli.menu.main_menu import MainMenu
from hspylib.modules.cli.menu.menu_ui import MenuUi

if __name__ == '__main__':
    mm = MenuUi(MainMenu())
    mm.show()

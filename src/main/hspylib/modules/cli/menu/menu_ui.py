#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu
      @file: menu_ui.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import signal
from typing import Optional

from hspylib.modules.cli.menu.menu import Menu
from hspylib.modules.cli.menu.menu_utils import MenuUtils


class MenuUi:
    def __init__(self, root: Optional[Menu]):
        self.done = False
        self.previous = None
        self.current = root
        self.next = None
        signal.signal(signal.SIGINT, MenuUtils.exit_app)
    
    def show(self) -> None:
        while not self.done:
            if self.current:
                self.next = self.current.execute()
                if self.next is None:
                    self.done = True
                else:
                    self.change_menu(self.next)
            else:
                self.done = True
    
    def change_menu(self, menu: Menu) -> None:
        self.previous = self.current
        self.current = menu

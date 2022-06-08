#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui
      @file: menu_ui.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import signal
from typing import Optional

from hspylib.modules.cli.tui.menu.menu import Menu
from hspylib.modules.cli.vt100.vt_utils import exit_app


class MenuUi:
    """TODO"""

    def __init__(self, root: Optional[Menu]):
        self.done = False
        self.previous = None
        self.current = root
        self.next = None
        signal.signal(signal.SIGINT, exit_app)

    def show(self) -> None:
        """TODO"""

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
        """TODO"""

        self.previous = self.current
        self.current = menu

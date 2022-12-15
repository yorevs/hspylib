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

from hspylib.modules.cli.tui.menu.menu import Menu
from hspylib.modules.cli.tui.tui_component import TUIComponent
from hspylib.modules.cli.vt100.vt_utils import exit_app
from typing import Optional

import signal


class TUIMenu(TUIComponent):
    """TODO"""

    def __init__(self, root: Optional[Menu]):
        super().__init__()
        self._curr_menu = root
        self._prev_menu = None
        self._next_menu = None
        signal.signal(signal.SIGINT, exit_app)

    def show(self) -> None:
        """TODO"""

        while not self.done:
            if self._curr_menu:
                self._next_menu = self._curr_menu.execute()
                if self._next_menu:
                    self.change_menu(self._next_menu)
                else:
                    self.done = True
            else:
                self.done = True

    def change_menu(self, menu: Menu) -> None:
        """TODO"""

        self._prev_menu = self._curr_menu
        self._curr_menu = menu

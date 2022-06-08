#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui
      @file: menu_item.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC, abstractmethod
from typing import Optional

from hspylib.core.exception.exceptions import InputAbortedError
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.tui.menu.menu import Menu
from hspylib.modules.cli.tui.menu.menu_utils import MenuUtils


class MenuItem(Menu, ABC):
    """TODO"""

    def __init__(self, parent: Menu = None, title: str = None):
        self.title = title
        self.parent = parent
        self.done = False
        self.selected = None
        self.items = None
        self.options = None
        self.menu_data = None

    def __str__(self):
        return self.menu_data if self.menu_data else ''

    def execute(self) -> Optional[Menu]:
        """TODO"""

        while self.selected != 0 and not self.done:
            sysout(str(self))
            try:
                self.selected = MenuUtils.prompt(end='$ ')
                if not self.selected:
                    continue
                if self.selected.isalnum() and self.is_valid_option():
                    return self.trigger_menu_item()
                MenuUtils.print_error("Invalid option", self.selected)
                self.selected = None
            except InputAbortedError:
                continue

    @abstractmethod
    def trigger_menu_item(self) -> Optional[Menu]:
        """TODO"""

    def is_valid_option(self) -> bool:
        """TODO"""
        if not self.options or not self.selected:
            return False
        if self.selected.isdigit():
            return int(self.selected) in self.options

        return str(self.selected) in self.options

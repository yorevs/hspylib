#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.factory
      @file: menu_factory.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.metaclass.singleton import Singleton
from hspylib.modules.cli.tui.menu.menu import Menu
from hspylib.modules.cli.tui.menu.menu_entry import MenuEntry
from hspylib.modules.cli.tui.menu.menu_option import MenuOption


class MenuFactory(metaclass=Singleton):
    """TODO"""

    class MenuBuilder:
        """TODO"""

        def __init__(self, parent_menu: Menu = None, menu_title: str = None):
            self.parent_menu = parent_menu
            self.menu_title = menu_title
            self.menu_options = {}

        def with_option(self, option_text: str) -> MenuOption:
            option_index = len(self.menu_options)
            option = MenuOption(self, option_index, option_text)
            self.menu_options[str(option_index)] = option
            return option

        def build(self) -> Menu:
            return MenuEntry(self.parent_menu, self.menu_options, self.menu_title)

    @staticmethod
    def create(parent_menu: Menu = None, menu_title: str = None) -> MenuBuilder:
        return MenuFactory.MenuBuilder(parent_menu, menu_title)

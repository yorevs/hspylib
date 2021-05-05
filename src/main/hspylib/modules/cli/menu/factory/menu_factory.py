#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.factory
      @file: menu_factory.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.meta.singleton import Singleton
from hspylib.modules.cli.menu.factory.menu_entry import MenuEntry
from hspylib.modules.cli.menu.factory.menu_option import MenuOption
from hspylib.modules.cli.menu.menu import Menu


class MenuFactory(metaclass=Singleton):
    class MenuBuilder:
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

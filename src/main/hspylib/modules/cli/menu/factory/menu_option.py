#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.factory
      @file: menu_option.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any


class MenuOption:
    def __init__(self, parent: Any, option_index: int, option_text: str):
        self.parent = parent
        self.option_index = option_index
        self.option_text = option_text
        self.action_trigger = lambda s: print(f"Option: {self.option_index}-{self.option_text} selected!")
    
    def on_trigger(self, action_trigger) -> Any:
        self.action_trigger = action_trigger
        return self.parent
    
    def __str__(self) -> str:
        return "%GREEN%[{}]%NC% {}".format(self.option_index, self.option_text)

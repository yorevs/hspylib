#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.factory
      @file: menu_option.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any


class MenuOption:
    """TODO"""

    def __init__(self, parent: Any, option_index: int, option_text: str):
        self.parent = parent
        self.option_index = option_index
        self.option_text = option_text
        self.action_trigger = lambda s: print(f"Option: {self.option_index}-{self.option_text} selected!")

    def on_trigger(self, action_trigger) -> Any:
        """TODO"""

        self.action_trigger = action_trigger
        return self.parent

    def __str__(self) -> str:
        return f"%GREEN%[{self.option_index}]%NC% {self.option_text}"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui
      @file: tui.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC, abstractmethod


class Menu(ABC):
    """TODO"""

    @abstractmethod
    def execute(self) -> 'Menu':
        """
        Execute the current tui actions.
        :return: The next tui action to proceed after processing.
        """

    @abstractmethod
    def trigger_menu_item(self) -> 'Menu':
        """
        Trigger the option action selected by the user.
        :return: The next tui action to trigger.
        """

    @abstractmethod
    def is_valid_option(self) -> bool:
        """
        Checks if the selected option is within the available menu_options.
        :return: whether the option is valid or not.
        """

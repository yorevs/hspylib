#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu_ui.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any, Optional

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.vt100.vt_utils import clear_screen, prepare_render

from clitt.core.tui.menu.tui_menu import TUIMenu
from clitt.core.tui.tui_preferences import TUIPreferences


class TUIMenuUi(metaclass=Singleton):
    """TODO"""

    app_title = "Main Menu"

    # fmt: off
    PREFS = TUIPreferences.INSTANCE or TUIPreferences()
    MENU_LINE = f"{'┅┅' * PREFS.title_line_length}"
    MENU_TITLE_FMT = (
        f"{PREFS.title_color}"
        f"┍{MENU_LINE}┓%EOL%"
        "┣{title:^" + str(2 * PREFS.title_line_length) + "s}┫%EOL%"
        f"┕{MENU_LINE}┙%EOL%%NC%"
    )
    # fmt: on

    @classmethod
    def render_app_title(cls) -> None:
        """TODO"""
        clear_screen()
        sysout(cls.MENU_TITLE_FMT.format(title=cls.app_title or "TITLE"))

    @staticmethod
    def back(source: TUIMenu) -> TUIMenu:
        """TODO"""
        return source.parent

    def __init__(self, main_menu: TUIMenu, title: str | None):
        check_not_none(main_menu)
        super().__init__()
        TUIMenuUi.app_title = title or "Main Menu"
        self._done: bool = False
        self._curr_menu: TUIMenu = main_menu
        self._prev_menu: Optional[TUIMenu] = None
        self._next_menu: Optional[TUIMenu] = None

    def execute(self) -> Any:
        """TODO"""

        prepare_render()

        while not self._done:
            if self._curr_menu:
                self._next_menu = self._curr_menu.execute()
                if self._next_menu:
                    self._change_menu(self._next_menu)
                else:
                    self._done = True
            else:
                self._done = True

        return None

    def _change_menu(self, menu: TUIMenu) -> None:
        """TODO"""
        self._prev_menu = self._curr_menu
        self._curr_menu = menu

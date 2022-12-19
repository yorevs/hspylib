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
from textwrap import dedent
from typing import List, Optional

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import hook_exit_signals, sysout
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu
from hspylib.modules.cli.tui.tui_component import T
from hspylib.modules.cli.tui.tui_preferences import TUIPreferences
from hspylib.modules.cli.vt100.vt_utils import exit_app, prepare_render, restore_cursor, restore_terminal, clear_screen
from hspylib.modules.eventbus import eventbus
from hspylib.modules.eventbus.event import Event


class TUIMenuUi(metaclass=Singleton):
    """TODO"""

    TITLE_LINE_SIZE = 20
    MENU_LINE = '-=' * TITLE_LINE_SIZE
    MENU_TITLE_FMT = (
        "{title_color}{menu_line}%EOL%"
        "{title:^" + str(2 * TITLE_LINE_SIZE) + "s}%EOL%"
        "{menu_line}%EOL%%NC%")

    @staticmethod
    @eventbus.subscribe(bus="tui-menu-ui", event="render-app-title")
    def render_title(event: Event) -> None:
        """TODO"""
        sysout(TUIMenuUi.MENU_TITLE_FMT)

    def __init__(self, main_menu: TUIMenu, title: str | None):
        check_not_none(main_menu)
        super().__init__()
        prefs = TUIPreferences.INSTANCE or TUIPreferences()
        TUIMenuUi.MENU_TITLE_FMT = TUIMenuUi.MENU_TITLE_FMT.format(
            title_color=prefs.title_color, title=title or "Main Menu", menu_line=TUIMenuUi.MENU_LINE)
        self._done: bool = False
        self._curr_menu: TUIMenu = main_menu
        self._prev_menu: Optional[TUIMenu] = None
        self._next_menu: Optional[TUIMenu] = None
        hook_exit_signals(exit_app)

    def execute(self) -> Optional[T | List[T]]:
        """TODO"""

        prepare_render()

        while not self._done:
            if self._curr_menu:
                clear_screen()
                self._next_menu = self._curr_menu.execute()
                if self._next_menu:
                    self._change_menu(self._next_menu)
                else:
                    self._done = True
            else:
                self._done = True

        restore_terminal()

        return None

    def _change_menu(self, menu: TUIMenu) -> None:
        """TODO"""
        self._prev_menu = self._curr_menu
        self._curr_menu = menu

    def _render(self) -> None:
        pass

    def _navbar(self, *args) -> str:
        pass

    def _handle_keypress(self) -> Keyboard:
        pass

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
from typing import List, Optional

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_not_none
from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu
from hspylib.modules.cli.tui.menu.tui_menu_utils import TUIMenuUtils
from hspylib.modules.cli.tui.tui_component import T
from hspylib.modules.cli.vt100.vt_utils import clear_screen, prepare_render
from hspylib.modules.eventbus import eventbus
from hspylib.modules.eventbus.event import Event


class TUIMenuUi(metaclass=Singleton):
    """TODO"""

    _app_title = "Main Menu"

    @staticmethod
    @eventbus.subscribe(bus="tui-menu-ui", event="render-app-title")
    def render_title(event: Event) -> None:
        """TODO"""
        TUIMenuUtils.title(TUIMenuUi._app_title)

    @staticmethod
    def back(source: TUIMenu) -> TUIMenu:
        return source.parent

    def __init__(self, main_menu: TUIMenu, title: str | None):
        check_not_none(main_menu)
        super().__init__()
        TUIMenuUi._app_title = title or "Main Menu"
        self._done: bool = False
        self._curr_menu: TUIMenu = main_menu
        self._prev_menu: Optional[TUIMenu] = None
        self._next_menu: Optional[TUIMenu] = None

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

        return None

    def _change_menu(self, menu: TUIMenu) -> None:
        """TODO"""
        self._prev_menu = self._curr_menu
        self._curr_menu = menu

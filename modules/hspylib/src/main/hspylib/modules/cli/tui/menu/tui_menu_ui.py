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

from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import hook_exit_signals
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.tui.menu.tui_menu import TUIMenu
from hspylib.modules.cli.tui.tui_component import T
from hspylib.modules.cli.vt100.vt_utils import clear_screen, exit_app, prepare_render, restore_cursor, restore_terminal


class TUIMenuUi:
    """TODO"""

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    TITLE_LINE_SIZE = 20

    MENU_TITLE_FMT = dedent("""
    {menu_line}
    {title:^""" + str(2 * TITLE_LINE_SIZE) + """s}
    {menu_line}

    """)

    def __init__(self, main_menu: TUIMenu):
        check_not_none(main_menu)
        super().__init__()
        self._done: bool = False
        self._curr_menu: TUIMenu = main_menu
        self._prev_menu: Optional[TUIMenu] = None
        self._next_menu: Optional[TUIMenu] = None
        hook_exit_signals(exit_app)

    def execute(self, title: str = "Main Menu") -> Optional[T | List[T]]:
        """TODO"""

        prepare_render(self.MENU_TITLE_FMT.format(menu_line='-=' * self.TITLE_LINE_SIZE, title=title))

        while not self._done:
            if self._curr_menu:
                restore_cursor()
                clear_screen(0)
                self._next_menu = self._curr_menu.execute(title)
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

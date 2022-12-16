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
from typing import Optional, List

from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import hook_exit_signals
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.tui.menu.tui_menu_item import TUIMenuItem
from hspylib.modules.cli.tui.tui_component import T
from hspylib.modules.cli.vt100.vt_utils import exit_app, prepare_render, restore_terminal, restore_cursor, clear_screen


class TUIMenu:
    """TODO"""

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    TITLE_LINE_SIZE = 20

    MENU_TITLE_FMT = dedent("""
    {menu_line}
    {title:^""" + str(2 * TITLE_LINE_SIZE) + """s}
    {menu_line}

    """)

    def __init__(self, main_menu: TUIMenuItem):
        check_not_none(main_menu)
        super().__init__()
        self._done = False
        self._curr_menu = main_menu
        self._prev_menu = None
        self._next_menu = None
        hook_exit_signals(exit_app)

    def execute(self, title: str = "Main Menu") -> Optional[T | List[T]]:

        prepare_render(self.MENU_TITLE_FMT.format(menu_line='-=' * self.TITLE_LINE_SIZE, title=title))

        while not self._done:
            if self._curr_menu:
                restore_cursor()
                clear_screen(0)
                self._next_menu = self._curr_menu.execute()
                if self._next_menu:
                    self._change_menu(self._next_menu)
                else:
                    self._done = True
            else:
                self._done = True

        restore_terminal()

        return None

    def _change_menu(self, menu: TUIMenuItem) -> None:
        """TODO"""
        self._prev_menu = self._curr_menu
        self._curr_menu = menu


if __name__ == '__main__':
    m = TUIMenuItem(title="Main Menu")
    s1 = TUIMenuItem(m, "Sub Menu One")
    s2 = TUIMenuItem(m, "Sub Menu Two")
    m.add_items(s1, s2)
    s1s1 = TUIMenuItem(s1, "Sub 1 Sub Menu One")
    s1s2 = TUIMenuItem(s1, "Sub 1 Sub Menu Two")
    back_s1 = TUIMenuItem(s1, "Back")
    back_s1.on_trigger(lambda: m)
    s1.add_items(s1s1, s1s2, back_s1)
    s2s1 = TUIMenuItem(s2, "Sub 2 Sub Menu One")
    s2s2 = TUIMenuItem(s2, "Sub 2 Sub Menu Two")
    back_s2 = TUIMenuItem(s2, "Back")
    back_s2.on_trigger(lambda: m)
    s2.add_items(s2s1, s2s2, back_s2)
    TUIMenu(m).execute('Testing Menus')

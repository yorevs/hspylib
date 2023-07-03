#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu_ui.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from clitt.core.tui.menu.tui_menu import TUIMenu
from clitt.core.tui.tui_preferences import TUIPreferences
from clitt.core.tui.tui_screen import TUIScreen
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.preconditions import check_not_none
from hspylib.modules.cli.vt100.vt_utils import set_auto_wrap, set_show_cursor


class TUIMenuUi(metaclass=Singleton):
    """Provide a menu for terminal UIs. Each sub-item must belong to the TUIMenu class and can be an instance of
    TUIMenuItem, TUIMenuAction or TUIMenuView.
    """

    app_title = "Main Menu"

    # fmt: off
    PREFS = TUIPreferences.INSTANCE or TUIPreferences()

    SCREEN = TUIScreen.INSTANCE or TUIScreen()

    MENU_LINE = f"{'-=' * PREFS.title_line_length}"

    MENU_TITLE_FMT = (
        f"{PREFS.title_color}"
        f"+{MENU_LINE}+%EOL%"
        "|{title:^" + str(2 * PREFS.title_line_length) + "s}|%EOL%"
        f"+{MENU_LINE}+%EOL%%NC%"
    )
    # fmt: on

    @classmethod
    def render_app_title(cls) -> None:
        """Render the application title."""
        cls.SCREEN.clear()
        cls.SCREEN.cursor.writeln(cls.MENU_TITLE_FMT.format(title=cls.app_title))

    @staticmethod
    def back(source: TUIMenu) -> TUIMenu:
        """Return the parent menu from the source of the event.
        :param source: the source menu of the event.
        """
        return source.parent

    def __init__(self, main_menu: TUIMenu, title: str = "Main Menu"):
        check_not_none(main_menu)
        super().__init__()
        TUIMenuUi.app_title = title
        self._done: bool = False
        self._curr_menu: TUIMenu = main_menu
        self._prev_menu = None
        self._next_menu = None

    def execute(self) -> None:
        """Execute the terminal menu UI flow."""

        self._prepare_render()

        while not self._done:
            if self._curr_menu:
                self._next_menu = self._curr_menu.execute()
                if self._next_menu:
                    self._change_menu(
                        self._next_menu
                        if isinstance(self._next_menu, TUIMenu)
                        else next((menu for menu in self._next_menu if menu), None)
                    )
                else:
                    self._done = True
            else:
                self._done = True

        self.SCREEN.cursor.end()
        self.SCREEN.cursor.write("%MOD(0)%")

    def _prepare_render(self) -> None:
        """Prepare the screen for renderization."""
        set_auto_wrap(True)
        set_show_cursor(False)
        self.SCREEN.clear()
        self.SCREEN.cursor.save()

    def _change_menu(self, new_menu: TUIMenu) -> None:
        """Change the current menu and keep track about the previous one.
        :param new_menu: the menu to be changed to.
        """
        self._prev_menu = self._curr_menu
        self._curr_menu = new_menu

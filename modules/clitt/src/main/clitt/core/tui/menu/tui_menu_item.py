#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.menu
      @file: tui_menu_item.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.term.commons import Direction, Portion
from clitt.core.tui.menu.tui_menu import TUIMenu
from clitt.core.tui.menu.tui_menu_ui import TUIMenuUi
from functools import cached_property
from hspylib.core.tools.dict_tools import get_or_default
from hspylib.modules.cli.keyboard import Keyboard
from typing import List, Optional


class TUIMenuItem(TUIMenu):
    """Represent a menu item with submenus. Each sub-item must belong to the TUIMenu class and can be an instance of
    TUIMenuItem, TUIMenuAction or TUIMenuView.
    """

    ROW_OFFSET = 5

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    def __init__(
        self,
        parent: Optional[TUIMenu] = None,
        title: str = "Sub Menu",
        tooltip: str = None,
        items: List[TUIMenu] = None,
    ):
        super().__init__(parent, title, tooltip or f"Access the '{title}' menu")
        self._show_from: int = 0
        self._show_to: int = self.screen.lines - self.ROW_OFFSET
        self._diff_index: int = self._show_to - self._show_from
        self._sel_index: int = 0
        self._items: List[TUIMenu] = items or []
        self._max_line_length = max(len(str(menu)) for menu in self._items) if self._items else len(str(self))

    @property
    def items(self) -> List[TUIMenu]:
        return self._items

    def add_items(self, *items: TUIMenu) -> None:
        """Add submenu items to the menu."""
        list(map(self._items.append, items))

    def execute(self) -> Optional[TUIMenu]:
        # Wait for user interaction
        while not self._done:
            if not self._items:
                return self._on_trigger(self._parent)

            # Menu Renderization
            if self._re_render:
                self.render()

            # Navigation input
            if self.handle_keypress() == Keyboard.VK_ENTER:
                return self._on_trigger(self._parent)

        return None

    def render(self) -> None:
        length = len(self._items)
        self.cursor.restore()
        TUIMenuUi.render_app_title()

        if length > 0:
            for idx in range(self._show_from, self._show_to):
                if idx >= length:
                    break  # When the number of items is lower than the max_rows, skip the other lines
                option_line = str(self._items[idx])
                self.cursor.erase(Portion.LINE)
                # Print the selector if the index is currently selected
                selector = self.draw_selector(is_selected=(idx == self._sel_index), has_bg_color=False)
                # fmt: off
                line_fmt = (
                    "  {:>" + f"{len(str(length))}" + "}  "
                    + "{:>" + f"{len(selector)}" + "}  "
                    + "{:<" + f"{self._max_line_length}" + "}  "
                )
                # fmt: on
                self.draw_line(line_fmt, idx + 1, selector, option_line)

        self.draw_navbar(self.navbar(to=length))
        self._re_render = False

    def navbar(self, **kwargs) -> str:
        menu = get_or_default(self.items, self._sel_index, None)
        tooltip = menu.tooltip if menu else None
        return (
            f"%EOL%%GREEN%{self.breadcrumb()} "
            f"{tooltip + ' ' if tooltip else ''}%ED0%%NC%"
            f"%EOL%{self.prefs.navbar_color.placeholder}%EOL%"
            f"[Enter] Select  Navigate  [{self.NAV_ICONS}]  "
            f"[Esc] Quit  [1..{kwargs['to']}] Goto: %NC%%EL0%%EOL%%EOL%"
        )

    def handle_keypress(self) -> Keyboard:
        """Handle a keyboard press."""
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case Keyboard.VK_ESC:
                    self._done = True
                case Keyboard.VK_UP:
                    self._handle_key_up()
                case Keyboard.VK_DOWN:
                    self._handle_key_down()
                case Keyboard.VK_TAB:
                    self._handle_tab()
                case Keyboard.VK_SHIFT_TAB:
                    self._handle_shift_tab()
                case _ as key if key in self._digits:
                    self._handle_digit(keypress)
            self._re_render = True

        return keypress

    def _handle_key_up(self) -> None:
        """Handle a key up (arrow up) press."""
        if self._sel_index == self._show_from and self._show_from > 0:
            self._show_from -= 1
            self._show_to -= 1
        if self._sel_index - 1 >= 0:
            self._sel_index -= 1
            self._re_render = True

    def _handle_key_down(self) -> None:
        """Handle a key down (arrow down) press."""
        length = len(self.items)
        if self._sel_index + 1 == self._show_to and self._show_to < length:
            self._show_from += 1
            self._show_to += 1
        if self._sel_index + 1 < length:
            self._sel_index += 1
            self._re_render = True

    def _handle_tab(self) -> None:
        """Handle a tab keypress."""
        length = len(self.items)
        page_index = min(self._show_to + self._diff_index, length)
        self._show_to = max(page_index, self._diff_index)
        self._show_from = self._show_to - self._diff_index
        self._sel_index = self._show_from
        self._re_render = True

    def _handle_shift_tab(self) -> None:
        """Handle a shift tab keypress."""
        page_index = max(self._show_from - self._diff_index, 0)
        self._show_from = min(page_index, self._diff_index)
        self._show_to = self._show_from + self._diff_index
        self._sel_index = self._show_from
        self._re_render = True

    def _handle_digit(self, digit: Keyboard) -> None:
        """Handle a digit keypress.
        :param digit: the digit pressed.
        """
        length = len(self._items)
        typed_index = digit.value
        self.write(digit.value)  # echo the digit typed
        index_len = 1
        while len(typed_index) < len(str(length)):
            keystroke = Keyboard.wait_keystroke()
            if not keystroke or not keystroke.isdigit():
                typed_index = None if keystroke != Keyboard.VK_ENTER else typed_index
                break
            typed_index = f"{typed_index}{keystroke.value if keystroke else ''}"
            self.write(f"{keystroke.value if keystroke else ''}")
            index_len += 1
        # Erase the index typed by the user
        self.cursor.move(index_len, Direction.LEFT)
        self.cursor.erase(Direction.RIGHT)
        if typed_index and 1 <= int(typed_index) <= length:
            self._show_to = max(int(typed_index), self._diff_index)
            self._show_from = self._show_to - self._diff_index
            self._sel_index = int(typed_index) - 1
            self._re_render = True

    def _default_trigger_cb(self, source: TUIMenu) -> Optional["TUIMenu"]:
        return get_or_default(self._items, self._sel_index, self._parent)

    @cached_property
    def _digits(self) -> List[Keyboard]:
        return Keyboard.digits()

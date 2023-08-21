#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.mselect
      @file: menu_select.py
   @created: Wed, 17 May 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.term.commons import Direction, Portion
from clitt.core.tui.tui_component import TUIComponent
from functools import cached_property
from hspylib.modules.cli.keyboard import Keyboard
from typing import List, Optional, TypeAlias, TypeVar

T = TypeVar("T")

MSelectItems: TypeAlias = List[T]


class MenuSelect(TUIComponent):
    """Terminal UI menu select input method"""

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    ROW_OFFSET = 5

    MIN_ROWS = 3

    def __init__(self, title: str, items: MSelectItems):
        super().__init__(title)
        self._items = items
        self._show_from = 0
        self._show_to = self._max_rows()
        self._diff_index = self._show_to - self._show_from
        self._sel_index = 0
        self._max_line_length = max(len(str(item)) for item in items)

    @cached_property
    def digits(self) -> List[Keyboard]:
        return Keyboard.digits()

    def execute(self) -> Optional[T]:
        """Execute the component's main flow."""

        if (length := len(self._items)) == 0:
            return None
        if length == 1:  # When only one option is provided, select the element at index 0 and return
            return self._items[0]

        self._prepare_render()
        keypress = self._loop()

        return self._items[self._sel_index] if keypress == Keyboard.VK_ENTER else None

    def render(self) -> None:
        """Renders the TUI component."""

        length = len(self._items)
        self.cursor.restore()
        self.writeln(f"{self.prefs.title_color.placeholder}{self.title}%EOL%%NC%")

        for idx in range(self._show_from, self._show_to):
            if idx >= length:
                break  # When the index is greater than the number of items, stop rendering

            option_line = str(self._items[idx])
            self.cursor.erase(Portion.LINE)
            # Print the selector if the index is currently selected
            selector = self.draw_selector(idx == self._sel_index)
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
        return (
            f"%EOL%{self.prefs.navbar_color.placeholder}"
            f"[Enter] Select  [{self.NAV_ICONS}] "
            f"Navigate  [Esc] Quit  [1..{kwargs['to']}] Goto: %NC%"
        )

    def handle_keypress(self) -> Keyboard:
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case _ as key if key in [Keyboard.VK_ESC, Keyboard.VK_ENTER]:
                    self._done = True
                case Keyboard.VK_UP:
                    self._handle_key_up()
                case Keyboard.VK_DOWN:
                    self._handle_key_down()
                case Keyboard.VK_TAB:
                    self._handle_tab()
                case Keyboard.VK_SHIFT_TAB:
                    self._handle_shift_tab()
                case _ as key if key in self.digits:
                    self._handle_digit(keypress)

        return keypress

    def _handle_digit(self, digit: Keyboard) -> None:
        """TODO"""
        length = len(self._items)
        typed_index = digit.value
        self.cursor.write(f"{digit.value}")  # echo the digit typed
        index_len = 1
        while len(typed_index) < len(str(length)):
            keystroke = Keyboard.wait_keystroke()
            if not keystroke or not keystroke.isdigit():
                typed_index = None if keystroke != Keyboard.VK_ENTER else typed_index
                break
            typed_index = f"{typed_index}{keystroke.value if keystroke else ''}"
            self.cursor.write(f"{keystroke.value if keystroke else ''}")
            index_len += 1
        # Erase the index typed by the user
        self.cursor.move(index_len, Direction.LEFT)
        self.cursor.erase(Direction.RIGHT)
        if typed_index and 1 <= int(typed_index) <= length:
            self._show_to = max(int(typed_index), self._diff_index)
            self._show_from = self._show_to - self._diff_index
            self._sel_index = int(typed_index) - 1
            self._re_render = True

    def _handle_key_up(self) -> None:
        """TODO"""
        if self._sel_index == self._show_from and self._show_from > 0:
            self._show_from -= 1
            self._show_to -= 1
        if self._sel_index - 1 >= 0:
            self._sel_index -= 1
            self._re_render = True

    def _handle_key_down(self) -> None:
        """TODO"""
        length = len(self._items)
        if self._sel_index + 1 == self._show_to and self._show_to < length:
            self._show_from += 1
            self._show_to += 1
        if self._sel_index + 1 < length:
            self._sel_index += 1
            self._re_render = True

    def _handle_tab(self) -> None:
        """TODO"""
        length = len(self._items)
        page_index = min(self._show_to + self._diff_index, length)
        self._show_to = max(page_index, self._diff_index)
        self._show_from = self._show_to - self._diff_index
        self._sel_index = self._show_from
        self._re_render = True

    def _handle_shift_tab(self) -> None:
        """TODO"""
        page_index = max(self._show_from - self._diff_index, 0)
        self._show_from = min(page_index, self._diff_index)
        self._show_to = self._show_from + self._diff_index
        self._sel_index = self._show_from
        self._re_render = True

    def _max_rows(self) -> int:
        screen_lines = self.screen.lines - self.ROW_OFFSET
        return min(self.prefs.max_rows, screen_lines)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.components
      @file: mchoose.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from functools import cached_property
from typing import List, Optional, TypeVar

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.tui_component import TUIComponent
from hspylib.modules.cli.vt100.vt_utils import prepare_render, restore_cursor, restore_terminal, screen_size

T = TypeVar("T")


def mchoose(
    items: List[T],
    checked: bool = True,
    title: str = "Please select one"
) -> Optional[List[T]]:
    """
    TODO
    :param items:
    :param checked:
    :param title:
    :return:
    """
    return MenuChoose(items, checked).execute(title)


class MenuChoose(TUIComponent):
    """TODO"""

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    def __init__(self, items: List[T], default_checked: bool):
        super().__init__()
        self.items = items
        self.show_from = 0
        self.show_to = self.prefs.max_rows
        self.diff_index = self.show_to - self.show_from
        self.sel_index = 0
        self.sel_options = [1 if default_checked else 0 for _ in range(len(items))]  # Initialize all options

    def execute(self, title: str) -> Optional[List[T]]:
        """TODO"""

        keypress = Keyboard.VK_NONE

        if len(self.items) == 0:
            return None

        prepare_render(title)

        # Wait for user interaction
        while not self.done and keypress not in [Keyboard.VK_ENTER, Keyboard.VK_ESC]:
            # Menu Renderization
            if self.require_render:
                self._render()

            # Navigation input
            keypress = self._handle_keypress()

        restore_terminal()

        return (
            [op for idx, op in enumerate(self.items) if self.sel_options[idx]]
            if keypress == Keyboard.VK_ENTER
            else None
        )

    def _render(self) -> None:
        """TODO"""

        length = len(self.items)
        _, columns = screen_size()
        restore_cursor()

        for idx in range(self.show_from, self.show_to):
            if idx >= length:
                break  # When the number of items is lower than the max_rows, skip the other lines
            else:
                option_line = str(self.items[idx])
                sysout("%EL2%\r", end="")  # Erase current line before repaint
                # Print the selector if the index is currently selected
                selector = self._draw_line_color(idx == self.sel_index)
                mark = self.prefs.marked if self.sel_options[idx] == 1 else self.prefs.unmarked
                # fmt: off
                line_fmt = (
                    "  {:>" + f"{len(str(length))}" + "}"
                    + "{:>" + f"{len(selector) + 1}" + "} "
                    + "{:>" + f"{len(str(mark))}" + "} {}"
                )
                # fmt: on
                self._draw_line(line_fmt, columns, idx + 1, selector, mark, option_line)

        sysout(self._navbar().replace('%TO%', str(length)), end="")
        self.require_render = False

    def _navbar(self) -> str:
        return \
            f"\n{self.prefs.navbar_color.placeholder}" \
            f"[Enter] Accept  [{self.NAV_ICONS}] " \
            f"Navigate  [Space] Mark  [I] Invert  [Esc] Quit  [1..%TO%] Goto: %EL0%"

    def _handle_keypress(self) -> Keyboard:
        """TODO"""

        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case _ as key if key in [Keyboard.VK_ESC, Keyboard.VK_ENTER]:
                    self.done = True
                case Keyboard.VK_UP:
                    self._handle_key_up()
                case Keyboard.VK_DOWN:
                    self._handle_key_down()
                case Keyboard.VK_TAB:
                    self._handle_tab()
                case Keyboard.VK_SHIFT_TAB:
                    self._handle_shift_tab()
                case Keyboard.VK_SPACE:
                    self._handle_space()
                case _ as key if key in [Keyboard.VK_i, Keyboard.VK_I]:
                    self._handle_i()
                case _ as key if key in self._digits:
                    self._handle_digit(keypress)

        return keypress

    def _handle_digit(self, keypress) -> None:
        """TODO"""
        length = len(self.items)
        typed_index = keypress.value
        sysout(f"{keypress.value}", end="")  # echo the digit typed
        index_len = 1
        while len(typed_index) < len(str(length)):
            keystroke = Keyboard.wait_keystroke()
            if not keystroke or not keystroke.isdigit():
                typed_index = None if keystroke != Keyboard.VK_ENTER else typed_index
                break
            typed_index = f"{typed_index}{keystroke.value if keystroke else ''}"
            sysout(f"{keystroke.value if keystroke else ''}", end="")
            index_len += 1
        # Erase the index typed by the user
        sysout(f"%CUB({index_len})%%EL0%", end="")
        if typed_index and 1 <= int(typed_index) <= length:
            self.show_to = max(int(typed_index), self.diff_index)
            self.show_from = self.show_to - self.diff_index
            self.sel_index = int(typed_index) - 1
            self.require_render = True

    def _handle_key_up(self) -> None:
        """TODO"""
        if self.sel_index == self.show_from and self.show_from > 0:
            self.show_from -= 1
            self.show_to -= 1
        if self.sel_index - 1 >= 0:
            self.sel_index -= 1
            self.require_render = True

    def _handle_key_down(self) -> None:
        """TODO"""
        length = len(self.items)
        if self.sel_index + 1 == self.show_to and self.show_to < length:
            self.show_from += 1
            self.show_to += 1
        if self.sel_index + 1 < length:
            self.sel_index += 1
            self.require_render = True

    def _handle_tab(self) -> None:
        """TODO"""
        length = len(self.items)
        page_index = min(self.show_to + self.diff_index, length)
        self.show_to = max(page_index, self.diff_index)
        self.show_from = self.show_to - self.diff_index
        self.sel_index = self.show_from
        self.require_render = True

    def _handle_shift_tab(self) -> None:
        """TODO"""
        page_index = max(self.show_from - self.diff_index, 0)
        self.show_from = min(page_index, self.diff_index)
        self.show_to = self.show_from + self.diff_index
        self.sel_index = self.show_from
        self.require_render = True

    def _handle_space(self) -> None:
        """TODO"""
        if self.sel_options[self.sel_index] == 0:
            self.sel_options[self.sel_index] = 1
        else:
            self.sel_options[self.sel_index] = 0
        self.require_render = True

    def _handle_i(self) -> None:
        """TODO"""
        self.sel_options = [(0 if op == 1 else 1) for op in self.sel_options]
        self.require_render = True

    @cached_property
    def _digits(self) -> List[Keyboard]:
        return Keyboard.digits()
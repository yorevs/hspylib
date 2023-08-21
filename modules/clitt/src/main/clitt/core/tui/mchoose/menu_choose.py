#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.mchoose
      @file: menu_choose.py
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

MChooseItems: TypeAlias = List[T]


class MenuChoose(TUIComponent):
    """Terminal UI menu choose input method."""

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.DOWN)

    ROW_OFFSET = 5

    MIN_ROWS = 3

    def __init__(self, title: str, items: MChooseItems, checked: bool):
        super().__init__(title)
        self.items = items
        self.show_from = 0
        self.show_to = self._max_rows()
        self.diff_index = self.show_to - self.show_from
        self.sel_index = 0
        self.sel_options = [1 if checked else 0 for _ in range(len(items))]  # Initialize all options
        self.max_line_length = max(len(str(item)) for item in items)

    @cached_property
    def digits(self) -> List[Keyboard]:
        return Keyboard.digits()

    def execute(self) -> Optional[MChooseItems]:
        if len(self.items) == 0:
            return None

        self._prepare_render()
        keypress = self._loop()

        return (
            [op for idx, op in enumerate(self.items) if self.sel_options[idx]]
            if keypress == Keyboard.VK_ENTER
            else None
        )

    def render(self) -> None:
        length = len(self.items)
        self.cursor.restore()
        self.writeln(f"{self.prefs.title_color.placeholder}{self.title}%EOL%%NC%")

        for idx in range(self.show_from, self.show_to):
            if idx >= length:
                break  # When the index is greater than the number of items, stop rendering

            option_line = str(self.items[idx])
            self.cursor.erase(Portion.LINE)
            # Print the selector if the index is currently selected
            selector = self.draw_selector(idx == self.sel_index)
            mark = self.prefs.checked_icon if self.sel_options[idx] == 1 else self.prefs.unchecked_icon
            # fmt: off
            line_fmt = (
                "  {:>" + f"{len(str(length))}" + "}  "
                + "{:>" + f"{len(selector)}" + "}  "
                + "{:>" + f"{len(str(mark))}" + "}  "
                + "{:<" + f"{self.max_line_length}" + "}  "
            )
            # fmt: on
            self.draw_line(line_fmt, idx + 1, selector, mark, option_line)

        self.draw_navbar(self.navbar(to=length))
        self._re_render = False

    def navbar(self, **kwargs) -> str:
        return (
            f"%EOL%{self.prefs.navbar_color.placeholder}"
            f"[Enter] Accept  [{self.NAV_ICONS}] "
            f"Navigate  [Space] Mark  [I] Invert  [Esc] Quit  [1..{kwargs['to']}] Goto: %NC%"
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
                case Keyboard.VK_SPACE:
                    self._handle_space()
                case _ as key if key in [Keyboard.VK_i, Keyboard.VK_I]:
                    self._handle_key_i()
                case _ as key if key in self.digits:
                    self._handle_digit(keypress)

        return keypress

    def _handle_digit(self, digit: Keyboard) -> None:
        """TODO"""
        length = len(self.items)
        typed_index = digit.value
        self.write(f"{digit.value}")  # echo the digit typed
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
            self.show_to = max(int(typed_index), self.diff_index)
            self.show_from = self.show_to - self.diff_index
            self.sel_index = int(typed_index) - 1
            self._re_render = True

    def _handle_key_up(self) -> None:
        """TODO"""
        if self.sel_index == self.show_from and self.show_from > 0:
            self.show_from -= 1
            self.show_to -= 1
        if self.sel_index - 1 >= 0:
            self.sel_index -= 1
            self._re_render = True

    def _handle_key_down(self) -> None:
        """TODO"""
        length = len(self.items)
        if self.sel_index + 1 == self.show_to and self.show_to < length:
            self.show_from += 1
            self.show_to += 1
        if self.sel_index + 1 < length:
            self.sel_index += 1
            self._re_render = True

    def _handle_tab(self) -> None:
        """TODO"""
        length = len(self.items)
        page_index = min(self.show_to + self.diff_index, length)
        self.show_to = max(page_index, self.diff_index)
        self.show_from = self.show_to - self.diff_index
        self.sel_index = self.show_from
        self._re_render = True

    def _handle_shift_tab(self) -> None:
        """TODO"""
        page_index = max(self.show_from - self.diff_index, 0)
        self.show_from = min(page_index, self.diff_index)
        self.show_to = self.show_from + self.diff_index
        self.sel_index = self.show_from
        self._re_render = True

    def _handle_space(self) -> None:
        """TODO"""
        if self.sel_options[self.sel_index] == 0:
            self.sel_options[self.sel_index] = 1
        else:
            self.sel_options[self.sel_index] = 0
        self._re_render = True

    def _handle_key_i(self) -> None:
        """TODO"""
        self.sel_options = [(0 if op == 1 else 1) for op in self.sel_options]
        self._re_render = True

    def _max_rows(self) -> int:
        screen_lines = self.screen.lines - self.ROW_OFFSET
        return min(self.prefs.max_rows, screen_lines)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.extra
      @file: mchoose.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import re
from abc import ABC
from typing import List, Optional, TypeVar

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import prepare_render, restore_cursor, restore_terminal, screen_size

T = TypeVar('T')


def mchoose(
    items: List[T],
    checked: bool = True,
    title: str = 'Please select one',
    max_rows: int = 15,
    title_color: VtColors = VtColors.ORANGE,
    highlight_color: VtColors = VtColors.BLUE,
    nav_color: VtColors = VtColors.YELLOW) -> Optional[List[T]]:
    """
    TODO
    :param items:
    :param checked:
    :param title:
    :param max_rows:
    :param title_color:
    :param highlight_color:
    :param nav_color:
    :return:
    """
    return MenuChoose(items, max_rows, checked).choose(title, title_color, highlight_color, nav_color)


class MenuChoose(ABC):
    """TODO"""
    UNSELECTED = ' '
    SELECTED = FormIcons.SELECTOR
    MARKED = FormIcons.MARKED
    UNMARKED = FormIcons.UNMARKED

    NAV_ICONS = '\u2191\u2193'
    NAV_FMT = "\n{}[Enter] Accept  [{}] Navigate  [Space] Mark  [I] Invert  [Q] Quit  [1..{}] Goto: %EL0%"

    def __init__(
        self,
        items: List[T],
        max_rows: int = 15,
        checked: bool = True):

        self.items = items
        self.checked = checked
        self.show_from = 0
        self.show_to = max_rows - 1
        self.diff_index = self.show_to - self.show_from
        self.sel_index = 0
        self.sel_options = [1 if self.checked else 0 for _ in range(len(items))]  # Initialize all options
        self.re_render = True
        self.done = None

    def choose(
        self,
        title: str,
        title_color: VtColors,
        highlight_color: VtColors,
        nav_color: VtColors) -> Optional[List[T]]:
        """TODO"""

        ret_val = Keyboard.VK_NONE
        length = len(self.items)

        if length == 0:
            return None

        prepare_render(title, title_color)

        # Wait for user interaction
        while not self.done and ret_val not in [Keyboard.VK_Q, Keyboard.VK_q, Keyboard.VK_ENTER, Keyboard.VK_ESC]:
            # Menu Renderization
            if self.re_render:
                self._render(highlight_color, nav_color)

            # Navigation input
            ret_val = self._nav_input()

        restore_terminal()

        return [op for idx, op in enumerate(self.items) if self.sel_options[idx]] \
            if ret_val == Keyboard.VK_ENTER else None

    def _render(self, highlight_color: VtColors, nav_color: VtColors) -> None:
        """TODO"""

        length = len(self.items)
        dummy, columns = screen_size()
        restore_cursor()

        for idx in range(self.show_from, self.show_to):
            selector = self.UNSELECTED

            if idx < length:  # When the number of items is lower than the max_rows, skip the other lines
                option_line = str(self.items[idx])[0:int(columns)]
                vt_print('%EL2%\r')  # Erase current line before repaint

                # Print the selector if the index is current
                if idx == self.sel_index:
                    vt_print(highlight_color.code())
                    selector = self.SELECTED

                # Print the marked or unmarked option
                mark = self.MARKED if self.sel_options[idx] == 1 else self.UNMARKED
                fmt = "  {:>" + str(len(str(length))) + "}{:>" \
                      + str(1 + len(str(selector))) + "} {:>" + str(len(str(mark))) + "} {}"
                sysout(fmt.format(idx + 1, selector, mark, option_line))

                # Check if the text fits the screen and print it, otherwise print '...'
                if len(option_line) >= int(columns):
                    sysout("%CUB(4)%%EL0%...", end='')
            else:
                break

        sysout(self.NAV_FMT.format(nav_color.placeholder(), self.NAV_ICONS, str(length)), end='')
        self.re_render = False

    # pylint: disable=too-many-branches
    def _nav_input(self) -> chr:
        """TODO"""

        length = len(self.items)
        keypress = Keyboard.read_keystroke()

        if keypress:
            if keypress in [Keyboard.VK_q, Keyboard.VK_Q, Keyboard.VK_ESC]:
                self.done = True
            elif keypress.isdigit():  # An index was typed
                typed_index = keypress.value
                sysout(f"{keypress.value}", end='')
                index_len = 1
                while len(typed_index) < len(str(length)):
                    numpress = Keyboard.read_keystroke()
                    if not numpress:
                        break
                    if not re.match(r'^[0-9]*$', numpress.value):
                        typed_index = None
                        break
                    typed_index = f"{typed_index}{numpress.value if numpress else ''}"
                    sysout(f"{numpress.value if numpress else ''}", end='')
                    index_len += 1
                # Erase the index typed by the user
                sysout(f"%CUB({index_len})%%EL0%", end='')
                if 1 <= int(typed_index) <= length:
                    self.show_to = max(int(typed_index), self.diff_index)
                    self.show_from = self.show_to - self.diff_index
                    self.sel_index = int(typed_index) - 1
                    self.re_render = True
            elif keypress == Keyboard.VK_SPACE:  # Space -> Mark option
                if self.sel_options[self.sel_index] == 0:
                    self.sel_options[self.sel_index] = 1
                else:
                    self.sel_options[self.sel_index] = 0
                self.re_render = True
            elif keypress in [Keyboard.VK_i, Keyboard.VK_I]:  # I -> Invert options
                self.sel_options = [(0 if op == 1 else 1) for op in self.sel_options]
                self.re_render = True
            elif keypress == Keyboard.VK_UP:  # Cursor up
                if self.sel_index == self.show_from and self.show_from > 0:
                    self.show_from -= 1
                    self.show_to -= 1
                if self.sel_index - 1 >= 0:
                    self.sel_index -= 1
                    self.re_render = True
            elif keypress == Keyboard.VK_DOWN:  # Cursor down
                if self.sel_index + 1 == self.show_to and self.show_to < length:
                    self.show_from += 1
                    self.show_to += 1
                if self.sel_index + 1 < length:
                    self.sel_index += 1
                    self.re_render = True
            elif keypress == Keyboard.VK_ENTER:  # Enter
                self.done = True

        self.re_render = True
        return keypress

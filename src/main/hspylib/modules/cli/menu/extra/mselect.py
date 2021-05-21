#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra
      @file: mselect.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
import signal
from abc import ABC
from typing import Any, List

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import screen_size


def mselect(
        items: List[Any],
        title: str = 'Please select one',
        max_rows: int = 15,
        title_color: VtColors = VtColors.ORANGE,
        highlight_color: VtColors = VtColors.BLUE,
        nav_color: VtColors = VtColors.YELLOW) -> Any:
    """
    TODO
    :param items:
    :param title:
    :param max_rows:
    :param title_color:
    :param highlight_color:
    :param nav_color:
    :return:
    """
    return MenuSelect(items, max_rows).select(title, title_color, highlight_color, nav_color)


class MenuSelect(ABC):

    UNSELECTED = ' '
    SELECTED = FormIcons.SELECTOR.value

    NAV_FMT = "{} [Enter] Select  [\u2191\u2193] Navigate  [Q] Quit  [1..{}] Goto: %EL0%"

    def __init__(
            self,
            items: List[Any],
            max_rows: int = 15):

        self.items = items
        self.show_from = 0
        self.show_to = max_rows - 1
        self.diff_index = self.show_to - self.show_from
        self.sel_index = 0
        self.re_render = True
        self.done = None

    def select(
            self,
            title: str = 'Please select one',
            title_color: VtColors = VtColors.ORANGE,
            highlight_color: VtColors = VtColors.BLUE,
            nav_color: VtColors = VtColors.YELLOW) -> Any:

        ret_val = None
        length = len(self.items)
        signal.signal(signal.SIGINT, MenuUtils.exit_app)
        signal.signal(signal.SIGHUP, MenuUtils.exit_app)
        
        if length > 0:

            # When only one option is provided, select the element at index 0 and return
            if length == 1:
                return self.items[0]

            sysout(f"%ED2%%HOM%{title_color.placeholder()}{title}")
            vt_print('%HOM%%CUD(1)%%ED0%')
            vt_print(Vt100.set_auto_wrap(False))
            vt_print(Vt100.set_show_cursor(False))
            vt_print(Vt100.save_cursor())

            # Wait for user interaction
            while not self.done and ret_val not in [Keyboard.VK_q, Keyboard.VK_Q, Keyboard.VK_ESC, Keyboard.VK_ENTER]:

                # Menu Renderization {
                if self.re_render:
                    self._render(highlight_color, nav_color)
                # } Menu Renderization

                # Navigation input {
                ret_val = self._nav_input()
                self.re_render = True
                # } Navigation input
        
        vt_print('%HOM%%ED2%%MOD(0)%')
        sysout(Vt100.set_show_cursor(True))
        
        return self.items[self.sel_index] \
            if self.sel_index >= 0 and ret_val == Keyboard.VK_ENTER else None
    
    def _render(
            self,
            highlight_color: VtColors,
            nav_color: VtColors) -> None:

        length = len(self.items)
        dummy, columns = screen_size()
        # Restore the cursor to the home position
        vt_print(Vt100.restore_cursor())
        sysout('%NC%')
        
        for idx in range(self.show_from, self.show_to):
            selector = self.UNSELECTED
            if idx >= length:
                break  # When the number of items is lower than the max_rows, skip the other lines
            option_line = str(self.items[idx])[0:int(columns)]
            vt_print('%EL2%\r')  # Erase current line before repaint
            # Print the selector if the index is currently selected
            if idx == self.sel_index:
                vt_print(highlight_color.code())
                selector = self.SELECTED
            fmt = " {:>" + str(len(str(length))) + "}{:>" + str(1 + len(str(selector))) + "} {}"
            sysout(fmt.format(idx + 1, selector, option_line))
            # Check if the text fits the screen and print it, otherwise print '...'
            if len(option_line) >= int(columns):
                vt_print("%CUB(4)%%EL0%...")
                sysout('%NC%')

        sysout('\n')
        sysout(MenuSelect.NAV_FMT.format(nav_color.placeholder(), str(length)), end='')
        self.re_render = False

    def _nav_input(self) -> chr:
        length = len(self.items)
        keypress = Keyboard.read_keystroke()

        if not keypress:
            return None

        if keypress in [Keyboard.VK_q, Keyboard.VK_Q, Keyboard.VK_ESC]:
            self.done = True
            sysout('\n%NC%')
        else:
            if keypress.isdigit():  # An index was typed
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
                sysout('\n%NC%')

        return keypress

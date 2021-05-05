#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra
      @file: mchoose.py
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
from hspylib.core.tools.keyboard import Keyboard
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import screen_size


def mchoose(
        items: List[Any],
        checked: bool = True,
        title: str = 'Please select one',
        max_rows: int = 15,
        title_color: VtColors = VtColors.ORANGE,
        highlight_color: VtColors = VtColors.BLUE,
        nav_color: VtColors = VtColors.YELLOW) -> List[Any]:
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
    return MenuChoose.choose(items, checked, title, max_rows, title_color, highlight_color, nav_color)


class MenuChoose(ABC):
    
    @classmethod
    def choose(
            cls,
            items: List[Any],
            checked: bool = True,
            title: str = 'Please select one',
            max_rows: int = 15,
            title_color: VtColors = VtColors.ORANGE,
            highlight_color: VtColors = VtColors.BLUE,
            nav_color: VtColors = VtColors.YELLOW) -> List[Any]:
        
        done = None
        show_from = 0
        sel_index = -1
        re_render = 1
        sel_options = []
        length = len(items)
        signal.signal(signal.SIGINT, MenuUtils.exit_app)
        
        if length > 0:
            sel_index = 0
            init_value = 1 if checked else 0
            show_to = max_rows - 1
            
            diff_index = show_to - show_from
            length = len(items)
            
            # Initialize all options
            sel_options = [init_value for _ in range(length)]
            
            sysout(f"%ED2%%HOM%{title_color.placeholder()}{title}")
            vt_print(Vt100.set_auto_wrap(False))
            vt_print('%HOM%%CUD(1)%%ED0%')
            vt_print(Vt100.save_cursor())
            
            # Wait for user interaction
            while not done:
                
                # Menu Renderization {
                if re_render:
                    cls.__render__(items, sel_options, show_from, show_to, sel_index, highlight_color)
                    sysout(
                        f"{nav_color.placeholder()} [Enter] Accept  [\u2191\u2193] Navigate  [Space] Mark  [I] Invert  [Q] Quit  [1..{str(length)}] Goto: %EL0%",
                        end='')
                    vt_print(Vt100.set_show_cursor(True))
                    re_render = None
                # } Menu Renderization
                
                # Navigation input {
                keypress = Keyboard.read_keystroke()
                if keypress in [Keyboard.VK_q, Keyboard.VK_Q, Keyboard.VK_ESC]:
                    done = True
                    sel_index = -1
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
                            show_to = max(int(typed_index), diff_index)
                            show_from = show_to - diff_index
                            sel_index = int(typed_index) - 1
                            re_render = 1
                    elif keypress == Keyboard.VK_SPACE:  # Space -> Mark option
                        if sel_options[sel_index] == 0:
                            sel_options[sel_index] = 1
                        else:
                            sel_options[sel_index] = 0
                        re_render = 1
                        continue
                    elif keypress in [Keyboard.VK_i, Keyboard.VK_I]:  # I -> Invert options
                        sel_options = [(0 if op == 1 else 1) for op in sel_options]
                        re_render = 1
                        continue
                    elif keypress == Keyboard.VK_UP:  # Cursor up
                        if sel_index == show_from and show_from > 0:
                            show_from -= 1
                            show_to -= 1
                        elif sel_index == 0:
                            continue
                        if sel_index - 1 >= 0:
                            sel_index -= 1
                            re_render = 1
                    elif keypress == Keyboard.VK_DOWN:  # Cursor down
                        if sel_index + 1 == show_to and show_to < length:
                            show_from += 1
                            show_to += 1
                        elif sel_index + 1 >= length:
                            continue
                        if sel_index + 1 < length:
                            sel_index += 1
                            re_render = 1
                    elif keypress == Keyboard.VK_ENTER:  # Enter
                        sysout('\n%NC%')
                        break
                # } Navigation input
        
        vt_print('%HOM%%ED2%%MOD(0)%')
        
        return [op for idx, op in enumerate(items) if sel_options[idx] == 1] if sel_index >= 0 else None
    
    @classmethod
    def __render__(
            cls,
            items: List[Any],
            sel_options: List[int],
            show_from: int,
            show_to: int,
            sel_index: int,
            highlight_color: VtColors = VtColors.BLUE) -> None:
        
        length = len(items)
        dummy, columns = screen_size()
        vt_print(Vt100.set_show_cursor(False))
        # Restore the cursor to the home position
        vt_print(Vt100.restore_cursor())
        sysout('%NC%')
        
        for idx in range(show_from, show_to):
            selector = ' '
            mark = ' '
            if idx >= length:
                break  # When the number of items is lower than the max_rows, skip the other lines
            option_line = str(items[idx])[0:int(columns)]
            # Erase current line before repaint
            vt_print('%EL2%\r')
            # Print the selector if the index is current
            if idx == sel_index:
                vt_print(highlight_color.code())
                selector = '>'
            # Print the marker if the option is checked
            if sel_options[idx] == 1:
                mark = 'x'
            fmt = " {:>" + str(len(str(length))) + "}  {:>2} [{}] {}"
            sysout(fmt.format(idx + 1, selector, mark, option_line))
            # Check if the text fits the screen and print it, otherwise print '...'
            if len(option_line) >= int(columns):
                vt_print("%CUB(4)%%EL0%...")
                sysout('%NC%')
        sysout('\n')

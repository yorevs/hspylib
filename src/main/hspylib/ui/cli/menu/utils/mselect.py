#!/usr/bin/env python3
import atexit
import curses
import os
from abc import ABC
from typing import Any, List

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.keyboard import Keyboard
from hspylib.ui.cli.vt100.vt_100 import Vt100
from hspylib.ui.cli.vt100.vt_codes import vt_print
from hspylib.ui.cli.vt100.vt_colors import VtColors


def mselect(*all_options) -> Any:
    """
    TODO
    :param all_options:
    :return:
    """
    items = [*all_options]
    return MenuSelect.select(items)


def foo(bar):
    print('hello {}'.format(bar))
    return 'foo'


class MenuSelect(ABC):

    @classmethod
    def select(cls, items: List[Any]) -> Any:
        ret_val = done = None
        sel_index = show_from = 0
        re_render = 1
        length = len(items)
        if length > 0:
            hl_color = os.environ.get('HHS_HIGHLIGHT_COLOR', VtColors.BLUE.code())
            max_rows = int(os.environ.get('HHS_MENU_MAXROWS', 15))
            show_to = max_rows - 1
            diff_index = show_to - show_from
            # When only one option is provided, select the element at index 0 and return
            if length == 1:
                return items[0]
            vt_print(Vt100.set_auto_wrap(False))
            vt_print('%HOM%%CUU(1)%%ED0%')
            vt_print(Vt100.save_cursor())
            # Wait for user interaction
            while not done:
                # Menu Renderization {
                if re_render:
                    rows, columns = os.popen('stty size').read().split()
                    vt_print(Vt100.set_show_cursor(False))
                    # Restore the cursor to the home position
                    vt_print(Vt100.restore_cursor())
                    sysout('%NC%')
                    for idx in range(show_from, show_to):
                        selector = ' '
                        if idx >= length:
                            break  # When the number of items is lower than the max_rows, skip the other lines
                        option_line = str(items[idx])  # [0:columns]
                        # Erase current line before repaint
                        vt_print('%EL2%\r')
                        if idx == sel_index:
                            sysout(hl_color)
                            selector = '>'
                        fmt = " {:>" + str(len(str(idx))) + "}  {:>4} {}"
                        sysout(fmt.format(idx + 1, selector, option_line))
                        # Check if the text fits the screen and print it, otherwise print '...'
                        if len(option_line) >= int(columns):
                            vt_print("%CUB(4)%%EL0%...")
                            sysout('%NC%')
                    sysout('\r')
                    sysout(f"%YELLOW%[Enter] Select  [↑↓] Navigate  [Q] Quit  [1..{str(length)}] Goto: %EL0%", end='')
                    re_render = None
                    vt_print(Vt100.set_show_cursor(True))
                # } Menu Renderization

                # Navigation input {
                key = Keyboard.read_keystroke()
                if key == Keyboard.VK_Q or key == Keyboard.VK_ESC:
                    done = True
                # } Navigation input

        return ret_val


if __name__ == '__main__':
    mselect('item1', 'item2')

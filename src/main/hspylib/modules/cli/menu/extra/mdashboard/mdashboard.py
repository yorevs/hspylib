#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra
      @file: mdashboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any, List

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.menu.extra.mdashboard.dashboard_builder import DashboardBuilder
from hspylib.modules.cli.menu.extra.mdashboard.dashboard_item import DashboardItem
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import set_enable_echo, restore_terminal, prepare_render, restore_cursor


def mdashboard(
        items: List[Any],
        items_per_line: int = 5,
        title: str = 'Please select one item',
        title_color: VtColors = VtColors.ORANGE,
        nav_color: VtColors = VtColors.YELLOW) -> Any:
    return MenuDashBoard(items, items_per_line).show(title, title_color, nav_color)


class MenuDashBoard:

    ICN = 'X'

    CELL_TPL = [
        [' ', ' ', ' ', ' ', ' ', ' ',' ', ' '],
        [' ', ' ', ' ', ICN, ' ', ' ',' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ',' ', ' ']
    ]
    
    SEL_CELL_TPL = [
        [' ', '\u250F', '\u2501', ' ', ' ', '\u2501', '\u2513', ' '],
        [' ', ' ', ' ', 'X', ' ', ' ', ' ', ' '],
        [' ', '\u2517', '\u2501', ' ', ' ', '\u2501', '\u251B', ' ']
    ]

    NAV_FMT = "\n{}[Enter] Select  [\u2190\u2191\u2192\u2193] Navigate  [Tab] Next  [Esc] Quit %EL0%"
    
    @classmethod
    def builder(cls):
        return DashboardBuilder()
    
    def __init__(
            self,
            items: List[Any],
            items_per_line: int = 5):
        
        self.items = items
        self.done = None
        self.re_render = True
        self.tab_index = 0
        self.items_per_line = items_per_line
        assert \
            len(self.CELL_TPL) == len(self.SEL_CELL_TPL) \
            and len(self.CELL_TPL[0]) == len(self.SEL_CELL_TPL[0]), \
            'Invalid CELL definitions. Selected and unselected matrices should have the same dimensions.'
    
    def show(
            self,
            title: str = 'Please select one item',
            title_color: VtColors = VtColors.ORANGE,
            nav_color: VtColors = VtColors.YELLOW) -> DashboardItem:

        ret_val = None
        length = len(self.items)

        if length > 0:
            prepare_render(title, title_color)
            
            # Wait for user interaction
            while not self.done and ret_val not in [Keyboard.VK_ENTER, Keyboard.VK_ESC]:
                # Menu Renderization
                if self.re_render:
                    self._render(nav_color)

                # Navigation input
                ret_val = self._nav_input()
                self.re_render = True

        restore_terminal()
        selected = self.items[self.tab_index] if ret_val == Keyboard.VK_ENTER else None

        if selected and selected.cb_action:
            selected.cb_action()

        return selected
    
    def _render(self, nav_color: VtColors) -> None:
        restore_cursor()
        set_enable_echo()

        for idx, item in enumerate(self.items):
            self._print_cell(idx, item, MenuDashBoard.CELL_TPL if self.tab_index != idx else MenuDashBoard.SEL_CELL_TPL)

        sysout(f'%EL2%\r> %GREEN%{self.items[self.tab_index].tooltip}%NC%')
        sysout(MenuDashBoard.NAV_FMT.format(nav_color.placeholder()), end='')
        self.re_render = False
    
    def _print_cell(self, idx: int, item: DashboardItem, cell_template: List[List[str]]) -> None:
        num_cols = len(cell_template[0])
        num_rows = len(cell_template)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                vt_print(f'{item.icon if cell_template[row][col] == self.ICN else cell_template[row][col]}')
            vt_print(f'%CUD(1)%%CUB({num_cols})%')

        if idx > 0 and (idx + 1) % self.items_per_line == 0:
            vt_print(f'%CUD(1)%%CUB({num_cols * self.items_per_line})%')  # Break the line
        elif idx + 1 < len(self.items):
            vt_print(f'%CUU({num_rows})%%CUF({num_cols})%')  # Continue with the same line

    def _nav_input(self) -> chr:
        length = len(self.items)
        keypress = Keyboard.read_keystroke()
        if keypress:
            if keypress == Keyboard.VK_ESC:
                self.done = True
            elif keypress == Keyboard.VK_UP:
                self.tab_index = max(0, self.tab_index - self.items_per_line)
            elif keypress == Keyboard.VK_DOWN:
                self.tab_index = min(length - 1, self.tab_index + self.items_per_line)
            elif keypress in [Keyboard.VK_LEFT, Keyboard.VK_SHIFT_TAB]:
                self.tab_index = max(0, self.tab_index - 1)
            elif keypress in [Keyboard.VK_RIGHT, Keyboard.VK_TAB]:
                self.tab_index = min(length - 1, self.tab_index + 1)
            elif keypress == Keyboard.VK_ENTER:
                pass  # Just exit
        
        self.re_render = True
        return keypress

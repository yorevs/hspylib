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

import signal
from typing import Any, Callable, List

from hspylib.core.tools.commons import sysout
from hspylib.core.tools.keyboard import Keyboard
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import set_enable_echo


def mdashboard(
        items: List[Any],
        items_per_line: int = 5,
        title: str = 'Please select one item',
        title_color: VtColors = VtColors.ORANGE,
        nav_color: VtColors = VtColors.YELLOW) -> Any:
    return MenuDashBoard(items, items_per_line).show(title, title_color, nav_color)


class MenuDashBoard:
    CELL_TPL = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', 'X', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]
    
    SEL_CELL_TPL = [
        [' ', '\u250F', '\u2501', ' ', ' ', '\u2501', '\u2513', ' '],
        [' ', ' ', ' ', 'X', ' ', ' ', ' ', ' '],
        [' ', '\u2517', '\u2501', ' ', ' ', '\u2501', '\u251B', ' ']
    ]
    
    @staticmethod
    class DashBoardItem:
        def __init__(
                self,
                icon: Awesome = None,
                tooltip: str = None,
                action: Callable = None):
            self.icon = icon
            self.tooltip = tooltip
            self.action = action
    
    @staticmethod
    class DashBoardBuilder:
        def __init__(self):
            self.items = []
        
        def item(self) -> Any:
            return MenuDashBoard.ItemBuilder(self)
        
        def build(self) -> list:
            return self.items
    
    @staticmethod
    class ItemBuilder:
        def __init__(self, parent: Any):
            self.parent = parent
            self.item = MenuDashBoard.DashBoardItem()
        
        def icon(self, icon: Awesome) -> Any:
            self.item.icon = icon
            return self
        
        def tooltip(self, tooltip: str) -> Any:
            self.item.tooltip = tooltip
            return self
        
        def action(self, action: Callable) -> Any:
            self.item.action = action
            return self
        
        def build(self) -> Any:
            self.parent.items.append(self.item)
            return self.parent
    
    @classmethod
    def builder(cls):
        return cls.DashBoardBuilder()
    
    def __init__(
            self,
            items: List[Any],
            items_per_line: int = 5):
        
        self.all_items = items
        self.done = None
        self.re_render = True
        self.tab_index = 0
        self.items_per_line = items_per_line
    
    def show(
            self,
            title: str = 'Please select one item',
            title_color: VtColors = VtColors.ORANGE,
            nav_color: VtColors = VtColors.YELLOW
    ) -> DashBoardItem:
        ret_val = None
        length = len(self.all_items)
        signal.signal(signal.SIGINT, MenuUtils.exit_app)
        signal.signal(signal.SIGHUP, MenuUtils.exit_app)
        
        if length > 0:
            sysout(f"%ED2%%HOM%{title_color.placeholder()}{title}")
            vt_print(Vt100.set_auto_wrap(False))
            vt_print('%HOM%%CUD(1)%%ED0%')
            vt_print(Vt100.save_cursor())
            
            # Wait for user interaction
            while not self.done and ret_val != Keyboard.VK_ENTER and ret_val != Keyboard.VK_ESC:
                # Menu Renderization {
                if self.re_render:
                    self.__render__(nav_color)
                # } Menu Renderization
                
                # Navigation input {
                ret_val = self.__nav_input__()
                self.re_render = True
                # } Navigation input
        
        vt_print('%HOM%%ED2%%MOD(0)%')
        vt_print(Vt100.set_show_cursor(True))
        
        selected = self.all_items[self.tab_index] if ret_val == Keyboard.VK_ENTER else None
        if selected and selected.action:
            selected.action()
        
        return selected
    
    def __render__(self, nav_color: VtColors) -> None:
        
        vt_print(Vt100.set_show_cursor(False))
        # Restore the cursor to the home position
        vt_print(Vt100.restore_cursor())
        sysout('%NC%')
        set_enable_echo()
        # Print cells
        for idx, item in enumerate(self.all_items):
            if self.tab_index != idx:
                self.__print_cell__(idx, item, MenuDashBoard.CELL_TPL)
            else:
                self.__print_cell__(idx, item, MenuDashBoard.SEL_CELL_TPL)
        # Print selected tab tooltip
        sysout(f'\r%EL2%> %GREEN%{self.all_items[self.tab_index].tooltip}%NC%\n\n')
        sysout(
            f"{nav_color.placeholder()}[Enter] Select  [\u2190\u2191\u2192\u2193] Navigate  [Tab] Next  [Esc] Quit %EL0%",
            end='')
    
    def __print_cell__(self, idx: int, item: DashBoardItem, cell_template: List[List[str]]) -> None:
        num_cols = len(cell_template[0])
        num_rows = len(cell_template)
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                if cell_template[row][col] == 'X':
                    vt_print(f'{item.icon}')
                else:
                    vt_print(f'{cell_template[row][col]}')
            vt_print(f'%CUD(1)%%CUB({num_cols})%')
        if idx > 0 and (idx + 1) % self.items_per_line == 0:
            # Break the line
            vt_print(f'%CUD(1)%%CUB({num_cols * self.items_per_line})%')
        elif idx + 1 < len(self.all_items):
            # Same line
            vt_print(f'%CUU({num_rows})%%CUF({num_cols})%')
        else:
            vt_print('%CUD(1)%%EL2%')
    
    def __nav_input__(self) -> chr:
        length = len(self.all_items)
        keypress = Keyboard.read_keystroke()
        
        if not keypress:
            return None
        
        if keypress == Keyboard.VK_ESC:
            self.done = True
            sysout('\n%NC%')
        else:
            if keypress == Keyboard.VK_TAB:  # Handle TAB
                if self.tab_index + 1 < length:
                    self.tab_index += 1
                else:
                    self.tab_index = 0
            elif keypress == Keyboard.VK_SHIFT_TAB:  # Handle Shift + TAB
                if self.tab_index - 1 >= 0:
                    self.tab_index -= 1
                else:
                    self.tab_index = length - 1
            elif keypress == Keyboard.VK_UP:  # Cursor up
                self.tab_index = max(0, self.tab_index - self.items_per_line)
            elif keypress == Keyboard.VK_DOWN:  # Cursor down
                self.tab_index = min(length - 1, self.tab_index + self.items_per_line)
            elif keypress == Keyboard.VK_LEFT:  # Cursor left
                self.tab_index = max(0, self.tab_index - 1)
            elif keypress == Keyboard.VK_RIGHT:  # Cursor right
                self.tab_index = min(length - 1, self.tab_index + 1)
            elif keypress == Keyboard.VK_ENTER:  # Select and exit
                pass
        
        return keypress

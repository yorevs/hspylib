#!/usr/bin/env python3
import signal
from typing import Any, Callable, List

from hspylib.core.tools.commons import sysout, set_enable_echo
from hspylib.core.tools.keyboard import Keyboard
from hspylib.ui.cli.icons.font_awesome.awesome import Awesome
from hspylib.ui.cli.icons.font_awesome.ui_compose.form_icons import FormIcons
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from hspylib.ui.cli.vt100.vt_100 import Vt100
from hspylib.ui.cli.vt100.vt_codes import vt_print
from hspylib.ui.cli.vt100.vt_colors import VtColors


def mdashboard():
    pass


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
        def __init__(self, icon: Awesome, tooltip: str, action: Callable):
            self.icon = icon
            self.tooltip = tooltip
            self.action = action

    def __init__(self, items: List[Any]):
        self.all_items = items
        self.done = None
        self.re_render = True
        self.tab_index = 0
        self.items_per_line = 3

    def show(
            self,
            title: str = 'Please select one item',
            title_color: VtColors = VtColors.ORANGE,
            nav_color: VtColors = VtColors.YELLOW
    ):
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

        return self.all_items[self.tab_index]

    def __render__(self, nav_color: VtColors):

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
        sysout(f'%EL2%>> %GREEN%{self.all_items[self.tab_index].tooltip} %NC%<<')
        sysout('\n')
        sysout(f"{nav_color.placeholder()}[Enter] Select  [\u2190\u2191\u2192\u2193] Navigate  [Tab] Next  [Esc] Quit %EL0%", end='')

    def __print_cell__(self, idx: int, item: DashBoardItem, cell_template: List[List[str]]):
        num_cols = len(cell_template[0])
        num_rows = len(cell_template)
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                if 'X' == cell_template[row][col]:
                    sysout(f'{item.icon}')
                else:
                    sysout(f'{cell_template[row][col]}')
            vt_print(f'%CUD(1)%%CUB({num_cols})%')
        if idx > 0 and (idx+1) % self.items_per_line == 0:
            # Break the line
            vt_print(f'%CUD(1)%%CUB({num_cols*self.items_per_line})%')
        else:
            # Same line
            vt_print(f'%CUU({num_rows})%%CUF({num_cols})%')

    def __nav_input__(self):
        length = len(self.all_items)
        keypress = Keyboard.read_keystroke()

        if not keypress:
            return None
        elif keypress == Keyboard.VK_ESC:
            self.done = True
            sysout('\n%NC%')
        else:
            if keypress == Keyboard.VK_TAB:  # Handle TAB
                if self.tab_index + 1 < length:
                    self.tab_index += 1
                else:
                    self.tab_index = 0
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


if __name__ == '__main__':
    i1 = MenuDashBoard.DashBoardItem(FormIcons.ON, 'Add something', lambda: print('Add'))
    i2 = MenuDashBoard.DashBoardItem(FormIcons.OFF, 'Remove something', lambda: print('Del'))
    i3 = MenuDashBoard.DashBoardItem(FormIcons.EDITABLE, 'Edit something', lambda: print('Edit'))
    i4 = MenuDashBoard.DashBoardItem(FormIcons.UNCHECK_CIRCLE, 'List something', lambda: print('List'))
    i5 = MenuDashBoard.DashBoardItem(FormIcons.EXIT, 'Update something', lambda: print('Update'))
    i6 = MenuDashBoard.DashBoardItem(FormIcons.VISIBLE, 'Back something', lambda: print('Back'))
    MenuDashBoard([
        i1, i2, i3, i4, i5, i6
    ]).show()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.components
      @file: mdashboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List, Optional

from hspylib.core.preconditions import check_state
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.nav_icons import NavIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.tui.mdashboard.dashboard_builder import DashboardBuilder
from hspylib.modules.cli.tui.mdashboard.dashboard_item import DashboardItem
from hspylib.modules.cli.vt100.vt_colors import VtColors
from hspylib.modules.cli.vt100.vt_utils import prepare_render, restore_cursor, restore_terminal, set_enable_echo


def mdashboard(
    items: List[DashboardItem],
    items_per_line: int = 5,
    title: str = "Please select one item",
    title_color: VtColors = VtColors.ORANGE,
    nav_color: VtColors = VtColors.YELLOW,
) -> Optional[DashboardItem]:
    """TODO"""

    return MenuDashBoard(items, items_per_line).execute(title, title_color, nav_color)


class MenuDashBoard:
    """TODO"""

    # fmt: off
    ICN = "X"

    CELL_TPL = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", ICN, " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]

    SEL_CELL_TPL = [
        [" ", "┏", "━", " ", " ", "━", "┓", " "],
        [" ", " ", " ", ICN, " ", " ", " ", " "],
        [" ", "┗", "━", " ", " ", "━", "┛", " "],
    ]
    # fmt: on

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.RIGHT, NavIcons.DOWN, NavIcons.LEFT)
    NAV_BAR = f"[Enter] Select  [{NAV_ICONS}] Navigate  [{NavIcons.TAB}] Next  [Esc] Quit %EL0%"

    @classmethod
    def builder(cls):
        """TODO"""
        return DashboardBuilder()

    def __init__(self, items: List[DashboardItem], items_per_line: int):

        self.items = items
        self.done = None
        self.re_render = True
        self.tab_index = 0
        self.items_per_line = items_per_line
        check_state(
            len(self.CELL_TPL) == len(self.SEL_CELL_TPL) and len(self.CELL_TPL[0]) == len(self.SEL_CELL_TPL[0]),
            "Invalid CELL definitions. Selected and Unselected matrices should have the same lengths.",
        )

    def execute(self, title: str, title_color: VtColors, nav_color: VtColors) -> Optional[DashboardItem]:
        """TODO"""

        keypress = Keyboard.VK_NONE

        if len(self.items) == 0:
            return None

        prepare_render(title, title_color)

        # Wait for user interaction
        while not self.done and keypress not in [Keyboard.VK_ENTER, Keyboard.VK_ESC]:
            # Menu Renderization
            if self.re_render:
                self._render(nav_color)

            # Navigation input
            keypress = self._handle_keypress()

        restore_terminal()
        selected = self.items[self.tab_index] if keypress == Keyboard.VK_ENTER else None

        if selected and selected.on_trigger:
            selected.on_trigger()

        return selected

    def _render(self, nav_color: VtColors) -> None:
        """TODO"""

        restore_cursor()
        set_enable_echo()

        for idx, item in enumerate(self.items):
            self._print_cell(idx, item, MenuDashBoard.CELL_TPL if self.tab_index != idx else MenuDashBoard.SEL_CELL_TPL)

        sysout(f"%EL2%\r> %GREEN%{self.items[self.tab_index].tooltip}%NC%")
        sysout(f"\n{nav_color.placeholder}{self.NAV_BAR}", end="")
        self.re_render = False

    def _handle_keypress(self) -> Keyboard:
        """TODO"""

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

    def _print_cell(self, idx: int, item: DashboardItem, cell_template: List[List[str]]) -> None:
        """TODO"""

        num_cols, num_rows = len(cell_template[0]), len(cell_template)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                sysout(f"{item.icon if cell_template[row][col] == self.ICN else cell_template[row][col]}", end="")
            sysout(f"%CUD(1)%%CUB({num_cols})%", end="")
        if idx > 0 and (idx + 1) % self.items_per_line == 0:
            sysout(f"%CUD(1)%%CUB({num_cols * self.items_per_line})%", end="")  # Break the line
        elif idx + 1 < len(self.items):
            sysout(f"%CUU({num_rows})%%CUF({num_cols})%", end="")  # Continue with the same line

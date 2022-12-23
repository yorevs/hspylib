#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.components
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
from hspylib.modules.cli.vt100.vt_utils import erase_line, prepare_render, restore_cursor

from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.keyboard import Keyboard
from clitt.core.tui.mdashboard.dashboard_builder import DashboardBuilder
from clitt.core.tui.mdashboard.dashboard_item import DashboardItem
from clitt.core.tui.tui_component import TUIComponent


def mdashboard(
    items: List[DashboardItem],
    title: str = "Please select one item"
) -> Optional[DashboardItem]:
    """TODO"""
    return MenuDashBoard(title, items).execute()


class MenuDashBoard(TUIComponent):
    """TODO"""

    # fmt: off
    ICN = "╳"

    CELL_TPL = [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", ICN, " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
    ]

    SEL_CELL_TPL = [
        [" ", "╭", " ", " ", " ", "╮", " "],
        [" ", " ", " ", ICN, " ", " ", " "],
        [" ", "╰", " ", " ", " ", "╯", " "],
    ]
    # fmt: on

    NAV_ICONS = NavIcons.compose(NavIcons.UP, NavIcons.RIGHT, NavIcons.DOWN, NavIcons.LEFT)

    @classmethod
    def builder(cls) -> DashboardBuilder:
        return DashboardBuilder()

    def __init__(self, title: str, items: List[DashboardItem]):
        super().__init__(title)
        self.items = items
        self.tab_index = 0
        check_state(
            len(self.CELL_TPL) == len(self.SEL_CELL_TPL) and len(self.CELL_TPL[0]) == len(self.SEL_CELL_TPL[0]),
            "Invalid CELL definitions. Selected and Unselected matrices should have the same lengths.",
        )

    def execute(self) -> Optional[DashboardItem]:

        if len(self.items) == 0:
            return None

        keypress = Keyboard.VK_NONE
        prepare_render()

        # Wait for user interaction
        while not self._done:
            # Menu Renderization
            if self._re_render:
                self._render()

            # Navigation input
            keypress = self._handle_keypress()

        selected = self.items[self.tab_index] if keypress == Keyboard.VK_ENTER else None

        if selected and selected.on_trigger:
            selected.on_trigger()

        return selected

    def _render(self) -> None:

        restore_cursor()
        sysout(f"{self.prefs.title_color.placeholder}{self.title}%NC%")

        for idx, item in enumerate(self.items):
            self._print_cell(
                idx, item,
                MenuDashBoard.CELL_TPL
                if self.tab_index != idx
                else MenuDashBoard.SEL_CELL_TPL
            )

        erase_line()
        sysout(self._navbar(), end="")
        self._re_render = False

    def _print_cell(
        self, item_idx: int,
        item: DashboardItem,
        cell_template: List[List[str]]) -> None:
        """TODO"""

        num_cols, num_rows = len(cell_template[0]), len(cell_template)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                cur_cell = cell_template[row][col]
                sysout(f"{item.icon if cur_cell == self.ICN else cur_cell}", end="")  # Print current cell
            sysout(f"%CUD(1)%%CUB({num_cols})%", end="")  # Print the next row
        if item_idx > 0 and (item_idx + 1) % self.prefs.items_per_line == 0:
            sysout(f"%CUD(1)%%CUB({num_cols * self.prefs.items_per_line})%", end="")  # Break the line
        elif item_idx + 1 < len(self.items):
            sysout(f"%CUU({num_rows})%%CUF({num_cols})%", end="")  # Continue with the same line

    def _navbar(self, **kwargs) -> str:
        return (
            f"{NavIcons.POINTER} %GREEN%{self.items[self.tab_index].tooltip}%NC%"
            f"%EOL%{self.prefs.navbar_color.placeholder}%EOL%"
            f"[Enter] Select  [Enter] "
            f"Navigate  [{self.NAV_ICONS}]  Next  [{NavIcons.TAB}]  [Esc] Quit %NC%%EL0%%EOL%%EOL%"
        )

    def _handle_keypress(self) -> Keyboard:
        length = len(self.items)
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case _ as key if key in [Keyboard.VK_ESC, Keyboard.VK_ENTER]:
                    self._done = True
                case Keyboard.VK_UP:
                    self.tab_index = max(0, self.tab_index - self.prefs.items_per_line)
                case Keyboard.VK_DOWN:
                    self.tab_index = min(length - 1, self.tab_index + self.prefs.items_per_line)
                case _ as key if key in [Keyboard.VK_LEFT, Keyboard.VK_SHIFT_TAB]:
                    self.tab_index = max(0, self.tab_index - 1)
                case _ as key if key in [Keyboard.VK_RIGHT, Keyboard.VK_TAB]:
                    self.tab_index = min(length - 1, self.tab_index + 1)

        self._re_render = True

        return keypress

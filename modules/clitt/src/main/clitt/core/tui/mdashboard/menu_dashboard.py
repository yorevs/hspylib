#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.mdashboard
      @file: menu_dashboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.term.commons import Direction, Portion
from clitt.core.tui.mdashboard.dashboard_builder import DashboardBuilder
from clitt.core.tui.mdashboard.dashboard_item import DashboardItem
from clitt.core.tui.tui_component import TUIComponent
from hspylib.core.preconditions import check_state
from hspylib.modules.cli.keyboard import Keyboard
from typing import List, Optional, TypeAlias

DashboardMatrix: TypeAlias = List[List[str]]


class MenuDashBoard(TUIComponent):
    """A dashboard is a type of graphical user interface which provides at-a-glance views."""

    # fmt: off
    ICN = "x"  # x mars the spot if the icon.

    # Selected cell template.
    CELL_TPL = [
        [" ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", ICN, " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " "],
    ]

    # Unselected cell template.
    SEL_CELL_TPL = [
        [" ", "╭", " ", " ", " ", "╮", " "],
        [" ", " ", " ", ICN, " ", " ", " "],
        [" ", "╰", " ", " ", " ", "╯", " "],
    ]
    # fmt: on

    NAV_ICONS = NavIcons.compose(NavIcons.LEFT, NavIcons.DOWN, NavIcons.UP, NavIcons.RIGHT)

    COLUMN_OFFSET = 10

    MIN_COLUMNS = 2

    @classmethod
    def builder(cls) -> DashboardBuilder:
        return DashboardBuilder()

    def __init__(self, title: str, items: List[DashboardItem]):
        super().__init__(title)
        self._items = items
        self._tab_index = 0
        check_state(
            len(self.CELL_TPL) == len(self.SEL_CELL_TPL) and len(self.CELL_TPL[0]) == len(self.SEL_CELL_TPL[0]),
            "Invalid CELL definitions. Selected and Unselected matrices should have the same lengths.",
        )

    def execute(self) -> Optional[DashboardItem]:
        if (len(self._items)) == 0:
            return None

        self._prepare_render()
        keypress = self._loop()
        selected = self._items[self._tab_index] if keypress == Keyboard.VK_ENTER else None

        if selected and selected.on_trigger:
            selected.on_trigger()

        return selected

    def render(self) -> None:
        self.cursor.restore()
        self.writeln(f"{self.prefs.title_color.placeholder}{self.title}%EOL%%NC%")

        for idx, item in enumerate(self._items):
            self._print_item(
                idx, item, MenuDashBoard.CELL_TPL if self._tab_index != idx else MenuDashBoard.SEL_CELL_TPL
            )

        self.cursor.erase(Portion.LINE)
        self.cursor.move_to(column=1)
        self.draw_navbar(self.navbar())
        self._re_render = False

    def navbar(self, **kwargs) -> str:
        return (
            f"{NavIcons.POINTER} %GREEN%{self._items[self._tab_index].tooltip}%NC%"
            f"%EOL%{self.prefs.navbar_color.placeholder}%EOL%"
            f"[Enter] Select  Navigate  {self.NAV_ICONS}  Next  [Tab]  [Esc] Quit %NC%"
        )

    def handle_keypress(self) -> Keyboard:
        length = len(self._items)
        if keypress := Keyboard.wait_keystroke():
            match keypress:
                case _ as key if key in [Keyboard.VK_ESC, Keyboard.VK_ENTER]:
                    self._done = True
                case Keyboard.VK_UP:
                    self._tab_index = max(0, self._tab_index - self._items_per_line())
                case Keyboard.VK_DOWN:
                    self._tab_index = min(length - 1, self._tab_index + self._items_per_line())
                case _ as key if key in [Keyboard.VK_LEFT, Keyboard.VK_SHIFT_TAB]:
                    self._tab_index = max(0, self._tab_index - 1)
                case _ as key if key in [Keyboard.VK_RIGHT, Keyboard.VK_TAB]:
                    self._tab_index = min(length - 1, self._tab_index + 1)

        self._re_render = True

        return keypress

    def _print_item(self, item_idx: int, item: DashboardItem, cell_template: DashboardMatrix) -> None:
        """Print the specified dashboard item at the given index.
        :param item_idx: the item index.
        :param item: the dashboard item.
        :param cell_template: the template of the dashboard cell (selected or unselected).
        """
        num_cols, num_rows = len(cell_template[0]), len(cell_template)
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                cur_cell = cell_template[row][col]
                # Print current cell
                self.write(f"{item.icon if cur_cell == self.ICN else cur_cell}")
            # Move to the next the next row
            self.cursor.move(1, Direction.DOWN)
            self.cursor.move(num_cols, Direction.LEFT)
        if item_idx > 0 and (item_idx + 1) % self._items_per_line() == 0:
            # Break the line
            self.cursor.move(1, Direction.DOWN)
            self.cursor.move(num_cols * self._items_per_line(), Direction.LEFT)
        elif item_idx + 1 < len(self._items):
            # Continue on the same line
            self.cursor.move(num_rows, Direction.UP)
            self.cursor.move(num_cols, Direction.RIGHT)

    def _items_per_line(self) -> int:
        screen_columns = self.screen.columns - self.COLUMN_OFFSET
        return max(self.MIN_COLUMNS, min(self.prefs.items_per_line, screen_columns))

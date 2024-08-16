#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.tui
      @file: tui_component.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os
from abc import ABC
from typing import Any, Optional, TypeVar

from clitt.core.icons.font_awesome.awesome import Awesome
from clitt.core.term.commons import Direction
from clitt.core.term.cursor import Cursor
from clitt.core.term.screen import Screen
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.tools.text_tools import elide_text
from hspylib.modules.cli.keyboard import Keyboard

T = TypeVar("T", bound=Any)


class TUIComponent(ABC):
    """Provide a base class for terminal UI components."""

    def __init__(self, title: str):
        self._re_render = True
        self._done = False
        self._title = title
        self._terminal = Terminal.INSTANCE

    @property
    def terminal(self) -> Terminal:
        return self._terminal

    @property
    def screen(self) -> Screen:
        return self.terminal.screen

    @property
    def cursor(self) -> Cursor:
        return self.terminal.screen.cursor

    @property
    def prefs(self) -> TUIPreferences:
        return self.screen.preferences

    @property
    def title(self) -> str:
        return self._title

    @property
    def rows(self) -> int:
        return self.screen.lines

    @property
    def columns(self) -> int:
        return self.screen.columns

    def _prepare_render(
        self,
        auto_wrap: bool = False,
        show_cursor: bool = False,
        clear_screen: bool = True
    ) -> None:
        """Prepare the screen for renderization."""
        self.screen.add_watcher(self.invalidate)
        Terminal.set_auto_wrap(auto_wrap)
        Terminal.set_show_cursor(show_cursor)
        if clear_screen:
            self.screen.clear()
        self.cursor.save()

    def _loop(self, break_keys: list[Keyboard] = None, cleanup: bool = True) -> Keyboard:
        """Loop and wait for a keypress. Render the component if required."""

        break_keys = break_keys or Keyboard.break_keys()
        keypress = Keyboard.VK_NONE

        # Wait for user interaction
        while not self._done and keypress not in break_keys:

            # Menu Renderization
            if self._re_render:
                self.render()
            # Navigation input
            keypress = self.handle_keypress()

        if cleanup:
            self.cursor.end()
            self.cursor.erase(Direction.DOWN)
            self.cursor.reset_mode()
            self.cursor.writeln(os.linesep)

        return keypress

    def draw_line(self, line_fmt: str, *args: Any) -> None:
        """Draws a formatted component line respecting the specified max_columns.
        :param line_fmt: the line format.
        :param args: the format arguments.
        """
        self.writeln(elide_text(line_fmt.format(*args), self.columns) + "%NC%")

    def draw_navbar(self, navbar: str) -> None:
        """Draws the component navigation bar respecting the specified max_columns.
        :param navbar: the component's navigation bar.
        """
        self.write(navbar)

    def draw_selector(self, is_selected: bool = False, has_bg_color: bool = True) -> Awesome:
        """Draws and highlight the selected component line.
        :param is_selected: whether to set a selected foreground color or not.
        :param has_bg_color: whether to set a background or not.
        """
        prefs = TUIPreferences.INSTANCE
        if is_selected:
            selector = prefs.selected_icon
            if has_bg_color:
                self.write(prefs.sel_bg_color.code)
            self.write(prefs.highlight_color.code)
        else:
            selector = prefs.unselected_icon
            self.write(prefs.text_color.code)

        return selector

    def write(self, obj: Any = "", end: str = "", markdown: bool = False) -> None:
        """Write the string representation of the object to the screen."""
        self.terminal.echo(obj, end=end, markdown=markdown)

    def writeln(self, obj: Any = "", markdown: bool = False) -> None:
        """Write the string representation of the object to the screen, appending a new line."""
        self.terminal.echo(obj, markdown=markdown)

    def invalidate(self) -> None:
        """Invalidate current TUI renderization."""
        self.screen.clear()
        self.cursor.save()
        self.cursor.track()
        self.render()

    def execute(self) -> Optional[T | list[T]]:
        """Execute the main TUI component flow."""
        ...

    def render(self) -> None:
        """Renders the TUI component."""
        ...

    def navbar(self, **kwargs) -> str:
        """Get the TUI component's navigation bar (optional)."""
        ...

    def handle_keypress(self) -> Keyboard:
        """Handle a keyboard press."""
        ...

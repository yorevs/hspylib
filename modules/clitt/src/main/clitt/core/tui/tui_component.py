#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.tui
      @file: tui_component.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from abc import ABC, abstractmethod
from clitt.core.icons.font_awesome.awesome import Awesome
from clitt.core.term.cursor import Cursor
from clitt.core.term.screen import Screen
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.tools.text_tools import elide_text
from hspylib.modules.cli.keyboard import Keyboard
from typing import Any, List, Optional, TypeVar

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

    def _prepare_render(self, auto_wrap: bool = False, show_cursor: bool = False) -> None:
        """Prepare the screen for renderization."""
        self.screen.add_watcher(self.invalidate)
        Terminal.set_auto_wrap(auto_wrap)
        Terminal.set_show_cursor(show_cursor)
        self.screen.clear()
        self.cursor.save()

    def _loop(self, break_keys: List[Keyboard] = None) -> Keyboard:
        """Loop and await for a keypress. Render the component if required."""

        break_keys = break_keys or [Keyboard.VK_ESC, Keyboard.VK_ENTER]
        keypress = Keyboard.VK_NONE

        # Wait for user interaction
        while not self._done and keypress not in break_keys:
            # Menu Renderization
            if self._re_render:
                self.render()

            # Navigation input
            keypress = self.handle_keypress()

        self.cursor.end()
        self.writeln("%MOD(0)%%EOL%")

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

    def write(self, obj: Any) -> None:
        """Write the string representation of the object to the screen."""
        self.terminal.echo(obj, end="")

    def writeln(self, obj: Any) -> None:
        """Write the string representation of the object to the screen, appending a new line."""
        self.terminal.echo(obj)

    def invalidate(self) -> None:
        """Invalidate current TUI renderization."""
        self.screen.clear()
        self.cursor.save()
        self.render()

    @abstractmethod
    def execute(self) -> Optional[T | List[T]]:
        """Execute the main TUI component flow."""

    @abstractmethod
    def render(self) -> None:
        """Renders the TUI component."""

    @abstractmethod
    def navbar(self, **kwargs) -> str:
        """Get the TUI component's navigation bar (optional)."""

    @abstractmethod
    def handle_keypress(self) -> Keyboard:
        """Handle a keyboard press."""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.tui
      @file: tui_screen.py
   @created: Thu, 22 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import last_index_of
from hspylib.modules.cli.vt100.vt_code import VtCode
from hspylib.modules.cli.vt100.vt_color import VtColor
from hspylib.modules.cli.vt100.vt_utils import (clear_screen, get_cursor_position, restore_cursor, restore_terminal,
                                                save_cursor, screen_size)
from threading import Timer
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union

import atexit
import os
import threading

DIMENSION = TypeVar("DIMENSION", bound=Tuple[int, ...])

POSITION = TypeVar("POSITION", bound=Tuple[int, int])

CB_RESIZE = TypeVar("CB_RESIZE", bound=Callable[[None], None])

MOVE_DIRECTION = TypeVar("MOVE_DIRECTION", bound="TUIScreen.CursorDirection")

ERASE_DIRECTION = TypeVar("ERASE_DIRECTION", bound=Union["TUIScreen.CursorDirection", "TUIScreen.ScreenPortion"])


class TUIScreen(metaclass=Singleton):
    """Provide a base class for terminal UI components."""

    INSTANCE = None

    RESIZE_WATCH_INTERVAL = 0.5

    class CursorDirection(Enumeration):
        """Provide a base class for the cursor direction."""

        # fmt: off
        UP          = '%ED1%', '%CUU({n})%'   # Cursor up (line)
        RIGHT       = '%EL0%', '%CUF({n})%'   # Cursor right (forward)
        DOWN        = '%ED0%', '%CUD({n})%'   # Cursor down (line)
        LEFT        = '%EL1%', '%CUB({n})%'   # Cursor left (backward)
        # fmt: on

    class ScreenPortion(Enumeration):
        """Provide a base class for the portions of the screen."""

        # fmt: off
        SCREEN      = '%ED2%', ''   # Entire screen (screen)
        LINE        = '%EL2%', ''   # Entire line (line)
        # fmt: on

    class Cursor(metaclass=Singleton):
        """Provide a base class for the screen cursor."""

        CURSOR_HOME = 1, 1

        def __init__(self):
            self._position: POSITION = get_cursor_position() or self.CURSOR_HOME
            self._bottom: POSITION = self.CURSOR_HOME
            self._saved_attrs = self._position, self._bottom

        def __str__(self):
            return f"({', '.join(list(map(str, self._position)))})"

        def __repr__(self):
            return str(self)

        @property
        def position(self) -> POSITION:
            return self._position

        @position.setter
        def position(self, new_position: POSITION) -> None:
            self._bottom = (new_position[0], new_position[1]) if new_position >= self._bottom else self._bottom
            self._position = new_position

        @property
        def bottom(self) -> POSITION:
            return self._bottom

        def home(self) -> None:
            """Move the cursor to home position."""
            self.move_to(self.CURSOR_HOME[0], self.CURSOR_HOME[1])

        def end(self) -> None:
            """Move the cursor to the bottom most position on the screen."""
            self.move_to(self.bottom[0], self.bottom[1])

        def move_to(self, row: int = None, column: int = None) -> POSITION:
            """Move the cursor to the specified position."""
            row_pos = max(self.CURSOR_HOME[0], row if row is not None else self.position[0])
            col_pos = max(self.CURSOR_HOME[1], column if column is not None else self.position[1])
            sysout(f"%CUP({row_pos};{col_pos})%", end="")
            self.position = row_pos, col_pos
            return self.position

        def move(self, amount: int, direction: MOVE_DIRECTION) -> POSITION:
            """Move the cursor towards the specified direction."""
            sysout(direction.value[1].format(n=amount), end="")
            row_pos, col_pos = self.position
            match direction:
                case TUIScreen.CursorDirection.UP:
                    row_pos -= max(0, amount)
                case TUIScreen.CursorDirection.DOWN:
                    row_pos += max(0, amount)
                case TUIScreen.CursorDirection.LEFT:
                    col_pos -= max(0, amount)
                case TUIScreen.CursorDirection.RIGHT:
                    col_pos += max(0, amount)
            self.position = row_pos, col_pos
            return self.position

        def erase(self, direction: ERASE_DIRECTION) -> POSITION:
            """Erase the screen following the specified direction.
            Note: It does not move the cursor along the way."""
            sysout(direction.value[0], end="")
            return self.position

        def track(self) -> POSITION:
            """Track the cursor position."""
            self.position = get_cursor_position() or self.position
            return self.position

        def write(self, obj: Any, end: str = "") -> POSITION:
            """Write the string representation of the object to the screen."""
            sysout(obj, end=end)
            text = (str(obj) + end).replace("%EOL%", os.linesep)
            text = VtColor.strip_colors(VtCode.strip_codes(text))
            text_offset = len(text[max(0, last_index_of(text, os.linesep)) :])
            self.position = self.position[0] + text.count(os.linesep), text_offset + (
                self.position[1] if text.count(os.linesep) == 0 else 0
            )
            return self.position

        def writeln(self, obj: Any) -> POSITION:
            """Write the string representation of the object to the screen, appending a new line."""
            return self.write(obj, end=os.linesep)

        def save(self) -> POSITION:
            """Save the current cursor position and attributes."""
            save_cursor()
            self._saved_attrs = self._position, self._bottom
            return self.position

        def restore(self) -> POSITION:
            """Save the current cursor position and attributes."""
            restore_cursor()
            self._position = self._saved_attrs[0]
            self._bottom = self._saved_attrs[1]
            return self.position

    def __init__(self):
        self._preferences: TUIPreferences = TUIPreferences.INSTANCE or TUIPreferences()
        self._dimension: DIMENSION = screen_size()
        self._cursor: TUIScreen.Cursor = self.Cursor()
        self._resize_timer: Optional[Timer] = None
        self._cb_watchers: List[CB_RESIZE] = []

        atexit.register(restore_terminal)
        self._resize_watcher()

    def __str__(self):
        return f"TUIScreen(rows={self.rows}, columns={self.columns}, cursor={self.cursor})"

    def __repr__(self):
        return str(self)

    @property
    def preferences(self) -> TUIPreferences:
        return self._preferences

    @property
    def dimension(self) -> DIMENSION:
        return self._dimension

    @property
    def rows(self) -> int:
        return self._dimension[0]

    @property
    def columns(self) -> int:
        return self._dimension[1]

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    def clear(self) -> None:
        """Clear the entire screen and move the cursor home."""
        clear_screen()
        self._cursor.home()

    def add_watcher(self, watcher: CB_RESIZE) -> None:
        """Add a resize watcher."""
        self._cb_watchers.append(watcher)
        if not self._resize_timer:
            self._resize_watcher()

    def _resize_watcher(self) -> None:
        """Add a watcher for screen resizes. If a resize is detected, the callback is called with the new dimension."""
        if self._cb_watchers and threading.main_thread().is_alive():
            dimension: DIMENSION = screen_size()
            self._resize_timer = Timer(self.RESIZE_WATCH_INTERVAL, self._resize_watcher)
            if dimension != self._dimension:
                list(map(lambda cb_w: cb_w(), self._cb_watchers))
                self._dimension = dimension
            self._resize_timer.start()

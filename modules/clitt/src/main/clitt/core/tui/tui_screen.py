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
import atexit
import os
import threading
from threading import Timer
from typing import Any, Callable, Tuple, TypeVar

from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import last_index_of
from hspylib.modules.cli.vt100.vt_code import VtCode
from hspylib.modules.cli.vt100.vt_utils import clear_screen, get_cursor_position, restore_terminal, save_cursor, \
    screen_size, set_auto_wrap, \
    set_show_cursor

from clitt.core.tui.tui_preferences import TUIPreferences

SCR_DIMENSION = TypeVar('SCR_DIMENSION', bound=Tuple[int, ...])

SCR_POSITION = TypeVar('SCR_POSITION', bound=Tuple[int, int])

CB_RESIZE = TypeVar('CB_RESIZE', bound=Callable[[Tuple[int, ...]], None])


class TUIScreen(metaclass=Singleton):
    """Provide a base class for terminal UI components."""

    SCREEN_REFRESH_TIME = 0.5

    @staticmethod
    def prepare_render(
        auto_wrap: bool = False,
        show_cursor: bool = False,
        is_clear_screen: bool = True,
        is_save_screen: bool = True):
        """Prepare the screen for TUI renderization."""

        atexit.register(restore_terminal)
        set_auto_wrap(auto_wrap)
        set_show_cursor(show_cursor)

        if is_clear_screen:
            clear_screen()
        if is_save_screen:
            save_cursor()

    class _Cursor(metaclass=Singleton):
        """Provide a base class for the screen cursor."""

        def __init__(self):
            self._position: SCR_POSITION = get_cursor_position() or (1, 1)

        def __str__(self):
            return f"({', '.join(list(map(str, self._position)))})"

        def __repr__(self):
            return str(self)

        @property
        def position(self) -> SCR_POSITION:
            return self._position

        def home(self) -> None:
            """TODO"""
            self.move(1, 1)

        def move(self, row: int = None, column: int = None) -> None:
            """TODO"""
            row_pos = max(1, row if row is not None else self._position[0])
            col_pos = max(1, column if column is not None else self._position[1])
            sysout(f"%CUP({row_pos};{col_pos})%", end="")
            self._position = row_pos, col_pos

        def track(self) -> SCR_POSITION:
            """TODO"""
            self._position = get_cursor_position() or (self._position[0], self._position[1])
            return self._position

        def write(self, obj: Any, end: str = '') -> SCR_POSITION:
            """TODO"""
            sysout(obj, end=end)
            text = VtCode.strip_codes(str(obj) + end)
            text_offset = len(text[max(0, last_index_of(text, os.linesep)):])
            self._position = \
                self._position[0] + text.count(os.linesep), \
                text_offset + (self._position[1] if text.count(os.linesep) == 0 else 0)
            return self.position

        def writeln(self, obj: Any) -> SCR_POSITION:
            """TODO"""
            return self.write(obj, end=os.linesep)

    def __init__(self, cb_resize: CB_RESIZE = None):
        self._prefs: TUIPreferences = TUIPreferences.INSTANCE or TUIPreferences()
        self._dimensions: tuple[int, ...] = screen_size()
        self._cursor = self._Cursor()
        self._resize_timer = None
        if cb_resize:
            self._resize_watcher(cb_resize)

    def __str__(self):
        return f"TUIScreen(rows={self.rows}, columns={self.columns}, cursor={self.cursor})"

    def __repr__(self):
        return str(self)

    @property
    def preferences(self) -> TUIPreferences:
        return self._prefs

    @property
    def dimensions(self) -> SCR_DIMENSION:
        return self._dimensions

    @property
    def rows(self) -> int:
        return self._dimensions[0]

    @property
    def columns(self) -> int:
        return self._dimensions[1]

    @property
    def cursor(self) -> _Cursor:
        return self._cursor

    def clear(self) -> None:
        clear_screen()
        self._cursor.home()

    def _resize_watcher(self, cb_watcher: CB_RESIZE) -> None:
        """TODO"""
        if threading.main_thread().is_alive():
            dimension: SCR_DIMENSION = screen_size()
            self._resize_timer = Timer(self.SCREEN_REFRESH_TIME, self._resize_watcher, [cb_watcher])
            if dimension != self._dimensions:
                cb_watcher(dimension)
                self._dimensions = dimension
            self._resize_timer.start()


if __name__ == '__main__':
    TUIScreen.prepare_render()
    screen = TUIScreen()
    screen.cursor.writeln(screen)
    screen.cursor.writeln(screen)
    screen.cursor.move(5, 18)
    screen.cursor.writeln(screen)
    screen.cursor.writeln(screen)
    print(get_cursor_position(), screen.cursor)

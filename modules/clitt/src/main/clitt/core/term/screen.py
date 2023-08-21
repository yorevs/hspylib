from clitt.core.term.commons import Dimension, get_dimensions, Portion, Resize_Cb
from clitt.core.term.cursor import Cursor
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from threading import Timer
from typing import List, Optional

import threading


class Screen(metaclass=Singleton):
    """Provide a base class for terminal UI components."""

    INSTANCE = None

    RESIZE_WATCH_INTERVAL = 0.5

    def __init__(self):
        self._preferences: TUIPreferences = TUIPreferences.INSTANCE
        self._dimension: Dimension = get_dimensions()
        self._cursor: Cursor = Cursor.INSTANCE or Cursor()
        self._resize_timer: Optional[Timer] = None
        self._cb_watchers: List[Resize_Cb] = []
        self._alternate: bool = False
        self._resize_watcher()

    def __str__(self):
        return f"Terminal.Screen(rows={self.lines}, columns={self.columns}, cursor={self.cursor})"

    def __repr__(self):
        return str(self)

    @property
    def preferences(self) -> TUIPreferences:
        return self._preferences

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @property
    def lines(self) -> int:
        return self._dimension[0]

    @property
    def columns(self) -> int:
        return self._dimension[1]

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    @property
    def alternate(self) -> bool:
        return self._alternate

    @alternate.setter
    def alternate(self, enable: bool) -> None:
        """Switch to the alternate screen buffer.
        :param enable: alternate enable on/off.
        """
        if enable != self._alternate:
            self._alternate = enable
            sysout(f"%SC{'A' if enable else 'M'}%", end="")
            self.cursor.track()

    def clear(self) -> None:
        """Clear terminal and move the cursor to HOME position (0, 0)."""
        self.cursor.home()
        self.cursor.erase(Portion.SCREEN)

    def add_watcher(self, watcher: Resize_Cb) -> None:
        """Add a resize watcher."""
        self._cb_watchers.append(watcher)
        if not self._resize_timer:
            self._resize_watcher()

    def _resize_watcher(self) -> None:
        """Add a watcher for screen resizes. If a resize is detected, the callback is called with the
        new dimension."""
        if self._cb_watchers and threading.main_thread().is_alive():
            dimension: Dimension = get_dimensions()
            self._resize_timer = Timer(self.RESIZE_WATCH_INTERVAL, self._resize_watcher)
            if dimension != self._dimension:
                list(map(lambda cb_w: cb_w(), self._cb_watchers))
                self._dimension = dimension
            self._resize_timer.start()

from clitt.core.term.commons import ERASE_DIRECTION, get_cursor_position, MOVE_DIRECTION, POSITION
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.text_tools import last_index_of
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_code import VtCode
from hspylib.modules.cli.vt100.vt_color import VtColor
from typing import Any

import os


class Cursor(metaclass=Singleton):
    """Provide a base class for the screen cursor."""

    INSTANCE = None

    CURSOR_HOME = 1, 1

    class Direction(Enumeration):
        """Provide a base class for the cursor direction."""

        # fmt: off
        UP          = '%ED1%', '%CUU({n})%'   # Cursor up (line)
        RIGHT       = '%EL0%', '%CUF({n})%'   # Cursor right (forward)
        DOWN        = '%ED0%', '%CUD({n})%'   # Cursor down (line)
        LEFT        = '%EL1%', '%CUB({n})%'   # Cursor left (backward)
        # fmt: on

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
            case Cursor.Direction.UP:
                row_pos -= max(0, amount)
            case Cursor.Direction.DOWN:
                row_pos += max(0, amount)
            case Cursor.Direction.LEFT:
                col_pos -= max(0, amount)
            case Cursor.Direction.RIGHT:
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
        sysout(Vt100.save_cursor(), end="")
        self._saved_attrs = self._position, self._bottom
        return self.position

    def restore(self) -> POSITION:
        """Save the current cursor position and attributes."""
        sysout(Vt100.restore_cursor(), end="")
        self._position = self._saved_attrs[0]
        self._bottom = self._saved_attrs[1]
        return self.position

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib-clitt
   @package: hspylib-clitt.main.clitt.core.term
      @file: cursor.py
   @created: Wed, 20 Mar 2024
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2024, HSPyLib team
"""

from clitt.core.term.commons import Direction, EraseDirection, get_cursor_position, MoveDirection, Portion, Position
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

    def __init__(self):
        self._position: Position = get_cursor_position() or self.CURSOR_HOME
        self._bottom: Position = self.CURSOR_HOME
        self._saved_attrs = self._position, self._bottom

    def __str__(self):
        return f"({', '.join(list(map(str, self._position)))})"

    def __repr__(self):
        return str(self)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, new_position: Position) -> None:
        self._bottom = (new_position[0], new_position[1]) if new_position >= self._bottom else self._bottom
        self._position = new_position

    @property
    def bottom(self) -> Position:
        return self._bottom

    def home(self) -> None:
        """Move the cursor to home position.
        :return None
        """
        self.move_to(self.CURSOR_HOME[0], self.CURSOR_HOME[1])

    def end(self) -> None:
        """Move the cursor to the bottom most position on the screen.
        :return None
        """
        self.move_to(self.bottom[0], self.bottom[1])

    def move_to(self, row: int = None, column: int = None) -> Position:
        """Move the cursor to the specified position.
        :param row the specified row to move.
        :param column the specified column to move.
        :return the cursor position after moving.
        """
        row_pos = max(self.CURSOR_HOME[0], row if row is not None else self.position[0])
        col_pos = max(self.CURSOR_HOME[1], column if column is not None else self.position[1])
        sysout(f"%CUP({row_pos};{col_pos})%", end="")
        self.position = row_pos, col_pos
        return self.position

    def move(self, amount: int, direction: MoveDirection) -> Position:
        """Move the cursor towards the specified direction.
        :param amount the amount of columns to move.
        :param direction the direction to move.
        :return the cursor position after moving.
        """
        if amount > 0:
            sysout(direction.value[1].format(n=amount), end="")
            row_pos, col_pos = self.position
            match direction:
                case Direction.UP:
                    row_pos -= max(0, amount)
                case Direction.DOWN:
                    row_pos += max(0, amount)
                case Direction.LEFT:
                    col_pos -= max(0, amount)
                case Direction.RIGHT:
                    col_pos += max(0, amount)
            self.position = row_pos, col_pos
        return self.position

    def erase(self, direction: EraseDirection) -> Position:
        """Erase the screen following the specified direction.
           Note: It does not move the cursor along the way.
        :param direction the direction to erase the screen.
        :return the cursor position after erasing.
        """
        sysout(direction.value[0], end="")
        return self.position

    def erase_line(self) -> Position:
        """Erase the previous line of the screen."""
        row_pos, col_pos = self.position
        self.move(1, Direction.UP)
        self.erase(Portion.LINE)
        self.move(col_pos, Direction.LEFT)
        self.position = row_pos, 0
        return self.position

    def track(self) -> Position:
        """Track the cursor position.
        :return the tracked cursor position.
        """
        self.position = get_cursor_position() or self.position
        return self.position

    def write(self, obj: Any = "", end: str = "", markdown: bool = False) -> Position:
        """Write the string representation of the object to the screen.
        :param obj the object to be written.
        :param end string appended after the last value, default a newline.
        :param markdown: whether to print a markdown render.
        :return the cursor position after writing.
        """
        sysout(obj, end=end, markdown=markdown)
        text: str = self.cleanup_text(str(obj) + end)
        text_offset: int = self.offset_text(text)
        self.position = self.position[0] + text.count(os.linesep), text_offset + (
            self.position[1] if text.count(os.linesep) == 0 else 0
        )
        return self.position

    def writeln(self, obj: Any = "", markdown: bool = False) -> Position:
        """Write the string representation of the object to the screen, appending a new line.
        :param obj the object to be written.
        :param markdown: whether to print a markdown render.
        :return the cursor position after writing.
        """
        return self.write(obj, end=os.linesep, markdown=markdown)

    def save(self) -> Position:
        """Save the current cursor position and attributes.
        :return the actual cursor position.
        """
        sysout(Vt100.save_cursor(), end="")
        self._saved_attrs = self._position, self._bottom
        return self.position

    def restore(self) -> Position:
        """Restore the saved cursor position and attributes.
        :return the cursor position after restoration.
        """
        sysout(Vt100.restore_cursor(), end="")
        self._position = self._saved_attrs[0]
        self._bottom = self._saved_attrs[1]
        return self.position

    def reset_mode(self, end="") -> Position:
        """Reset cursor modifiers."""
        sysout(Vt100.mode(0), end=end)
        return self.position

    def cleanup_text(self, text: str) -> str:
        """TODO"""
        return VtColor.strip_colors(VtCode.strip_codes(text.replace("%EOL%", os.linesep)))

    def offset_text(self, text: str) -> int:
        """TODO"""
        text: str = self.cleanup_text(text)
        return len(text[max(0, last_index_of(text, os.linesep)):])


assert (cursor := Cursor().INSTANCE) is not None, "Failed to create Cursor instance"

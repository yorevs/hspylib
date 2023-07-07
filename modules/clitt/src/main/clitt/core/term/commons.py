from clitt.core.exception.exceptions import NotATerminalError
from hspylib.core.tools.commons import is_debugging
from hspylib.modules.cli.vt100.vt_100 import Vt100
from shutil import get_terminal_size
from typing import Callable, Tuple, TypeVar, Union

import logging as log
import re
import sys
import termios
import tty

DIMENSION = TypeVar("DIMENSION", bound=Tuple[int, int])

POSITION = TypeVar("POSITION", bound=Tuple[int, int])

CB_RESIZE = TypeVar("CB_RESIZE", bound=Callable[[None], None])

MOVE_DIRECTION = TypeVar("MOVE_DIRECTION", bound="Cursor.Direction")

ERASE_DIRECTION = TypeVar("ERASE_DIRECTION", bound=Union["Cursor.Direction", "Screen.Portion"])


def get_dimensions(fallback: Tuple[int, int] = (24, 80)) -> Tuple[int, int]:
    """Retrieve the size of the terminal.
    :return lines, columns
    """
    if not sys.stdout.isatty():
        log.warning(NotATerminalError("get_dimensions:: Requires a terminal (TTY)"))
        return fallback
    dim = get_terminal_size((fallback[1], fallback[0]))
    return dim.lines, dim.columns


def get_cursor_position(fallback: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    """Get the terminal cursor position.
    :return line, column
    """
    pos, buf, re_query_resp = fallback, "", r"^\x1b\[(\d*);(\d*)R"

    if not sys.stdout.isatty():
        log.warning(NotATerminalError("get_cursor_position:: Requires a terminal (TTY)"))
        return pos

    if is_debugging():
        return pos

    stdin = sys.stdin.fileno()  # Get the stdin file descriptor.
    attrs = termios.tcgetattr(stdin)  # Save terminal attributes.

    try:
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write(Vt100.get_cursor_pos())
        sys.stdout.flush()
        while not buf or buf[-1] != "R":
            buf += sys.stdin.read(1)
        if matches := re.match(re_query_resp, buf):  # If the response is 'Esc[r;cR'
            groups = matches.groups()
            pos = int(groups[0]), int(groups[1])
    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, attrs)  # Reset terminal attributes

    return pos

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib-clitt
   @package: hspylib-clitt.main.clitt.core.term
      @file: commons.py
   @created: Wed, 20 Mar 2024
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2024, HSPyLib team
"""

import re
import sys
import termios
import tty
from shutil import get_terminal_size
from typing import Callable, Tuple, TypeAlias, Union

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.commons import is_debugging
from hspylib.modules.cli.vt100.vt_100 import Vt100

# fmt: off
Dimension       : TypeAlias = Tuple[int, int]
Position        : TypeAlias = Tuple[int, int]
Resize_Cb       : TypeAlias = Callable[[], None]
MoveDirection   : TypeAlias = "Direction"
EraseDirection  : TypeAlias = Union["Direction", "Portion"]
# fmt: on


def is_a_tty() -> bool:
    """Checks whether we are under a tty environment."""
    try:
        return sys.stdout.isatty() and sys.stdin.isatty()
    except ValueError:
        return sys.stdout.isatty()


class Direction(Enumeration):
    """Provide a base class for the cursor direction."""

    # fmt: off
    UP          = '%ED1%', '%CUU({n})%'   # Cursor up (line)
    RIGHT       = '%EL0%', '%CUF({n})%'   # Cursor right (forward)
    DOWN        = '%ED0%', '%CUD({n})%'   # Cursor down (line)
    LEFT        = '%EL1%', '%CUB({n})%'   # Cursor left (backward)
    # fmt: on


class Portion(Enumeration):
    """Provide a base class for the portions of the screen."""

    # fmt: off
    SCREEN      = '%ED2%', ''   # Entire screen (screen)
    LINE        = '%EL2%', ''   # Entire line (line)
    # fmt: on


def get_dimensions(fallback: Tuple[int, int] = (24, 80)) -> Tuple[int, int]:
    """Retrieve the size of the terminal.
    :return lines, columns
    """
    if not is_a_tty():
        return fallback
    dim = get_terminal_size((fallback[1], fallback[0]))
    return dim.lines, dim.columns


def get_cursor_position(fallback: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    """Get the terminal cursor position.
    :return line, column
    """
    pos = fallback

    if is_debugging():
        return pos

    if not is_a_tty():
        return pos

    buf, re_query_resp = "", r"^\x1b\[(\d*);(\d*)R"
    stdin, attrs = None, None

    try:
        stdin = sys.stdin.fileno()  # Get the stdin file descriptor.
        attrs = termios.tcgetattr(stdin)  # Save terminal attributes.
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write(Vt100.get_cursor_pos())
        sys.stdout.flush()
        while not buf or buf[-1] != "R":
            buf += sys.stdin.read(1)
        if matches := re.match(re_query_resp, buf):  # If the response is 'Esc[r;cR'
            groups = matches.groups()
            pos = int(groups[0]), int(groups[1])
    except termios.error:
        pass
    finally:
        if stdin and attrs:
            termios.tcsetattr(stdin, termios.TCSANOW, attrs)  # Reset terminal attributes

    return pos

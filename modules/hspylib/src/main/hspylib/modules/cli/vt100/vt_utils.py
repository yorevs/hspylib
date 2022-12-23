#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.vt100
      @file: vt_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import atexit
import os
import re
import sys
import termios
import tty
from typing import Any, Optional, Tuple

from hspylib.core.exception.exceptions import NotATerminalError
from hspylib.core.tools.commons import is_debugging, sysout
from hspylib.modules.cli.vt100.vt_100 import Vt100


def screen_size() -> tuple[int, ...]:
    """Retrieve the size of the terminal"""
    if not sys.stdout.isatty():
        raise NotATerminalError("screen_size:: Requires a terminal (TTY)")

    return tuple(map(int, os.popen("stty size").read().split()))


# Solution taken from:
# https://stackoverflow.com/questions/46651602/determine-the-terminal-cursor-position-with-an-ansi-sequence-in-python-3
def get_cursor_position() -> Optional[Tuple[int, int]]:
    """Get the terminal cursor position"""
    if not sys.stdout.isatty():
        raise NotATerminalError("get_cursor_position:: Requires a terminal (TTY)")

    if is_debugging():
        return 0, 0
    buf = ""
    stdin = sys.stdin.fileno()
    attrs = termios.tcgetattr(stdin)
    try:
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write(Vt100.get_cursor_pos())  # Query the terminal
        sys.stdout.flush()
        while True:
            buf += sys.stdin.read(1)
            if buf[-1] == "R":
                break
        matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
        groups = matches.groups()
        return int(groups[0]), int(groups[1])
    except AttributeError:
        return None
    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, attrs)


def set_enable_echo(enabled: bool = True) -> None:
    """Enable echo in the terminal
    :param enabled: whether is enabled or not
    """
    if not sys.stdout.isatty():
        raise NotATerminalError("set_enable_echo:: Requires a terminal (TTY)")

    os.popen(f"stty {'echo -raw' if enabled else 'raw -echo min 0'}").read()


def set_auto_wrap(auto_wrap: bool = True) -> None:
    """Set auto-wrap mode in the terminal
    :param auto_wrap: whether auto_wrap is set or not
    """
    sysout(Vt100.set_auto_wrap(auto_wrap), end="")


def set_show_cursor(show_cursor: bool = True) -> None:
    """Show or hide cursor in the terminal
    :param show_cursor: whether to show or hide he cursor
    """
    sysout(Vt100.set_show_cursor(show_cursor), end="")


def erase_line(mode: int = 2) -> None:
    """Erase current line"""
    sysout(f"%EL{mode}%\r", end="")


def save_cursor() -> None:
    """Save cursor position and attributes"""
    sysout(Vt100.save_cursor(), end="")


def clear_screen(mode: int = 2) -> None:
    """Clear terminal"""
    sysout(f"%CUP(0;0)%%ED{mode}%", end="")


def restore_cursor() -> None:
    """Restore cursor position and attributes"""
    sysout(Vt100.restore_cursor(), end="")


def alternate_screen(enable: bool = True) -> None:
    """Switch to the alternate screen buffer on/off"""
    sysout(f"%SC{'A' if enable else 'M'}%", end="")


def restore_terminal() -> None:
    """Clear the terminal and restore default attributes"""
    set_auto_wrap()
    set_show_cursor()
    set_enable_echo()
    sysout("%MOD(0)%")


def exit_app(exit_code: int = None, frame: Any = None, exit_msg: str = "") -> None:
    """Exit the application. Commonly called by hooked signals"""
    sysout(f"{exit_msg if exit_msg else ''}", end="")
    sysout("%MOD(0)%")
    restore_terminal()
    sys.exit(exit_code)


def prepare_render():
    """Prepare the terminal for TUI renderization"""
    atexit.register(restore_terminal)
    set_auto_wrap(False)
    set_show_cursor(False)
    clear_screen()
    save_cursor()

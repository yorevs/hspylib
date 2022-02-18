#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.vt100
      @file: vt_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
import re
import signal
import sys
import termios
import tty
from typing import List, Optional, Tuple

from hspylib.core.tools.commons import is_debugging, sysout
from hspylib.modules.cli.vt100.vt_100 import Vt100
from hspylib.modules.cli.vt100.vt_codes import vt_print
from hspylib.modules.cli.vt100.vt_colors import VtColors


def require_terminal():
    if not sys.stdin.isatty():
        raise Exception('This module requires a terminal (TTY)')


def screen_size() -> Optional[List[str]]:
    """Retrieve the size of the terminal"""
    if sys.stdout.isatty():
        return os.popen('stty size').read().split()

    return None


# Solution taken from:
# https://stackoverflow.com/questions/46651602/determine-the-terminal-cursor-position-with-an-ansi-sequence-in-python-3
def get_cursor_position() -> Optional[Tuple[int, int]]:
    """ Get the terminal cursor position """
    if sys.stdout.isatty() and not is_debugging():
        buf = ""
        stdin = sys.stdin.fileno()
        attrs = termios.tcgetattr(stdin)
        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()
            while True:
                buf += sys.stdin.read(1)
                if buf[-1] == "R":
                    break
        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, attrs)
        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
            groups = matches.groups()
        except AttributeError:
            return None
        return int(groups[0]), int(groups[1])

    return None


def set_enable_echo(enabled: bool = True) -> None:
    """Enable echo in the terminal
    :param enabled: whether is enabled or not
    """
    if sys.stdout.isatty():
        os.popen(f"stty {'echo -raw' if enabled else 'raw -echo min 0'}").read()


def set_auto_wrap(auto_wrap: bool = True) -> None:
    """Set auto-wrap mode in the terminal
    :param auto_wrap: whether auto_wrap is set or not
    """
    vt_print(Vt100.set_auto_wrap(auto_wrap))


def set_show_cursor(show_cursor: bool = True):
    """Show or hide cursor in the terminal
    :param show_cursor: whether to show or hide he cursor
    """
    vt_print(Vt100.set_show_cursor(show_cursor))


def save_cursor():
    """Save cursor position and attributes"""
    vt_print(Vt100.save_cursor())


def restore_cursor():
    """Restore cursor position and attributes"""
    vt_print(Vt100.restore_cursor())


def restore_terminal(clear_screen: bool = True):
    """Clear terminal and restore default attributes"""
    if clear_screen:
        vt_print('%HOM%%ED2%%MOD(0)%')
    set_auto_wrap()
    set_show_cursor()
    set_enable_echo()
    sysout('%NC%')


def exit_app(exit_code: int = signal.SIGHUP, frame=None, exit_msg: str = "Done.") -> None:
    """Exit the application. Commonly hooked to signals"""
    sysout(str(frame) if frame else '', end='')
    sysout(f"%HOM%%ED2%%NC%\n{exit_msg}\n")
    restore_terminal(False)
    sys.exit(exit_code if exit_code else 0)


def prepare_render(render_msg: str = '', render_color: VtColors = VtColors.ORANGE):
    """Prepare the terminal for TUI renderization"""
    signal.signal(signal.SIGINT, exit_app)
    signal.signal(signal.SIGHUP, exit_app)
    set_auto_wrap(False)
    set_show_cursor(False)
    sysout(f"%ED2%%HOM%{render_color.placeholder()}{render_msg}%HOM%%CUD(1)%%ED0%")
    save_cursor()

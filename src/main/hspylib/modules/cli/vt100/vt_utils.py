#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.vt100
      @file: vt_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
import re
import sys
import termios
import tty
from typing import List, Optional, Tuple

assert sys.stdin.isatty(), 'This module requires a terminal (TTY)'


def require_terminal():
    assert sys.stdin.isatty(), 'This module requires a terminal (TTY)'


def screen_size() -> Optional[List[str]]:
    """Retrieve the size of the terminal"""
    if sys.stdout.isatty():
        return os.popen('stty size').read().split()
    
    return None


def get_cursor_position() -> Optional[Tuple[int, int]]:
    """ Get the terminal cursor position
    Solution taken from:
    - https://stackoverflow.com/questions/46651602/determine-the-terminal-cursor-position-with-an-ansi-sequence-in-python-3
    """
    if sys.stdout.isatty():
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


def set_enable_echo(enable: bool = True) -> None:
    """Enable echo in the terminal
    :param enable:
    """
    if sys.stdout.isatty():
        os.popen(f"stty {'echo -raw' if enable else 'raw -echo min 0'}").read()

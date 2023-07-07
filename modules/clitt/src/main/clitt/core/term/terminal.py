#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.cli.vt100
      @file: terminal.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.exception.exceptions import NotATerminalError
from clitt.core.term.cursor import Cursor
from clitt.core.term.screen import Screen
from hspylib.core.enums.charset import Charset
from hspylib.core.metaclass.singleton import Singleton
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.vt_100 import Vt100
from typing import Any, Optional, Tuple

import atexit
import logging as log
import os
import platform
import select
import shlex
import signal
import subprocess
import sys


class Terminal(metaclass=Singleton):
    """Utility class to provide terminal features."""

    INSTANCE = None

    @staticmethod
    def is_a_tty() -> bool:
        return sys.stdout.isatty()

    @staticmethod
    def shell_exec(cmd_line: str, **kwargs) -> Tuple[Optional[str], ExitStatus]:
        """Execute command with arguments and return it's run status."""
        try:
            if "stdout" in kwargs:
                del kwargs["stdout"]  # Deleted since we use our own stream
            if "stderr" in kwargs:
                del kwargs["stderr"]  # Deleted since we use our own stream
            log.info("Executing shell command: %s", cmd_line)
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            output = subprocess.check_output(cmd_args, **kwargs).decode(Charset.UTF_8.val)
            log.info("Execution result: %s", ExitStatus.SUCCESS)
            return output.strip() if output else None, ExitStatus.SUCCESS
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)
            return None, ExitStatus.FAILED

    @staticmethod
    def shell_poll(cmd_line: str, **kwargs) -> None:
        """Execute command with arguments and continuously poll it's output."""
        if "stdout" in kwargs:
            del kwargs["stdout"]  # Deleted since we use our own stream
        if "stderr" in kwargs:
            del kwargs["stderr"]  # Deleted since we use our own stream
        try:
            log.info("Polling shell command: %s", cmd_line)
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            with subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs) as proc:
                process = select.poll()
                process.register(proc.stdout)
                process.register(proc.stderr)
                while not Keyboard.kbhit():
                    if poll_obj := process.poll(0.5):
                        line = proc.stdout.readline()
                        sysout(line.decode(Charset.UTF_8.val) if isinstance(line, bytes) else line.strip(), end="")
                        log.debug("Polling returned: %s", str(poll_obj))
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except (InterruptedError, KeyboardInterrupt):
            log.warning("Polling process has been interrupted command='%s'", cmd_line)
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)

    @staticmethod
    def open(filename: str) -> None:
        """Open the specified file using the default editor."""
        my_os = os.environ.get("HHS_MY_OS", platform.system())
        if "Darwin" == my_os:
            Terminal.shell_exec(f"open {filename}")
        elif "Linux" == my_os:
            Terminal.shell_exec(f"xdg-open {filename}")
        else:
            raise NotImplementedError(f"OS '{my_os}' is not supported")

    @classmethod
    def restore(cls) -> None:
        """Clear the terminal and restore default attributes [wrap,cursor,echo]."""
        cls.set_attributes(show_cursor=True, auto_wrap=True, enable_echo=True)
        cls.alternate_screen(False)
        sysout("%MOD(0)%", end="")

    @classmethod
    def set_enable_echo(cls, enabled: bool = True) -> None:
        """Enable echo in the terminal.
        :param enabled: whether is enabled or not.
        """
        if not cls.is_a_tty():
            log.warning(NotATerminalError("set_enable_echo:: Requires a terminal (TTY)"))
            return

        os.popen(f"stty {'echo -raw' if enabled else 'raw -echo min 0'}").read()

    @classmethod
    def set_auto_wrap(cls, auto_wrap: bool = True) -> None:
        """Set auto-wrap mode in the terminal.
        :param auto_wrap: whether auto_wrap is set or not.
        """
        if not cls.is_a_tty():
            log.warning(NotATerminalError("set_auto_wrap:: Requires a terminal (TTY)"))
            return

        sysout(Vt100.set_auto_wrap(auto_wrap), end="")

    @classmethod
    def set_show_cursor(cls, show_cursor: bool = True) -> None:
        """Show or hide cursor in the terminal.
        :param show_cursor: whether to show or hide he cursor.
        """
        if not cls.is_a_tty():
            log.warning(NotATerminalError("set_show_cursor:: Requires a terminal (TTY)"))
            return

        sysout(Vt100.set_show_cursor(show_cursor), end="")

    @classmethod
    def set_attributes(cls, **attrs) -> None:
        """Wrapper to set all terminal attributes at once."""
        # fmt: off
        enable_echo = attrs['enable_echo']
        auto_wrap   = attrs['auto_wrap']
        show_cursor = attrs['show_cursor']
        # fmt: on
        if enable_echo is not None:
            cls.set_enable_echo(enable_echo)
        if auto_wrap is not None:
            cls.set_auto_wrap(auto_wrap)
        if show_cursor is not None:
            cls.set_show_cursor(show_cursor)

    @classmethod
    def clear(cls) -> None:
        """Clear terminal and move the cursor to HOME position (0, 0)."""
        cls.INSTANCE.screen.clear()

    @classmethod
    def echo(cls, obj: Any, end: str = os.linesep) -> None:
        """Write the string representation of the object to the screen."""
        cls.INSTANCE.screen.cursor.write(obj, end=end)

    @classmethod
    def alternate_screen(cls, enable: bool) -> None:
        """Switch to the alternate screen buffer on/off."""
        cls.INSTANCE.screen.alternate = enable

    def __init__(self):
        self._screen = Screen.INSTANCE or Screen()
        atexit.register(self.restore)

    @property
    def screen(self) -> Screen:
        return self._screen

    @property
    def cursor(self) -> Cursor:
        return self.screen.cursor


assert Terminal().INSTANCE is not None, "Failed to create Terminal instance"

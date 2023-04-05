#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.vt100
      @file: terminal.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import logging as log
import os
import platform
import select
import shlex
import signal
import subprocess
from abc import ABC
from typing import Optional, Tuple

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.cli.keyboard import Keyboard


class Terminal(ABC):
    """Utility class to provide execution of commands on a terminal"""

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
            with (subprocess.Popen(
                    cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid, **kwargs)) as proc:
                process = select.poll()
                process.register(proc.stdout)
                while not Keyboard.kbhit():
                    if poll_obj := process.poll(0.3):
                        line = bytes(proc.stdout.readline()).decode(Charset.UTF_8.val).strip()
                        sysout(line)
                        log.debug("Polling returned: %s", str(poll_obj))
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except (InterruptedError, KeyboardInterrupt):
            log.warning("Polling process has been interrupted command='%s'", cmd_line)
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)

    @staticmethod
    def open_file(filename: str):
        """Open the specified file using the default editor."""
        my_os = os.environ.get("HHS_MY_OS", platform.system())
        if "Darwin" == my_os:
            Terminal.shell_exec(f"open {filename}")
        elif "Linux" == my_os:
            Terminal.shell_exec(f"xdg-open {filename}")
        else:
            raise NotImplementedError(f"OS '{my_os}' is not supported")

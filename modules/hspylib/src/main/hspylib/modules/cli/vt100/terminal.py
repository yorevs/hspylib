#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.vt100
      @file: terminal.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC
from hspylib.core.tools.commons import syserr
from hspylib.modules.application.exit_status import ExitStatus
from typing import Optional, Tuple

import logging as log
import os
import platform
import select
import shlex
import subprocess


class Terminal(ABC):
    """Utility class to provide execution of commands on a terminal"""

    @staticmethod
    def shell_exec(cmd_line: str, **kwargs) -> Tuple[Optional[str], ExitStatus]:
        """Execute command with arguments and return it's run status."""
        try:
            log.info("Executing shell command: %s", cmd_line)
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            output = subprocess.check_output(cmd_args, **kwargs).decode("utf-8")
            log.info("Execution result: %s", ExitStatus.SUCCESS)
            return output.strip() if output else None, ExitStatus.SUCCESS
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)
            syserr(str(err))
            return None, ExitStatus.FAILED

    @staticmethod
    def shell_poll(cmd_line: str, **kwargs) -> None:
        """Execute command with arguments and continuously poll it's output."""
        if "stdout" in kwargs:
            del kwargs["stdout"]  # Deleted since we use our own
        if "stderr" in kwargs:
            del kwargs["stderr"]  # Deleted since we use our own
        try:
            log.info("Polling shell command: %s", cmd_line)
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            with (subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)) as file:
                process = select.poll()
                process.register(file.stdout)
                while True:
                    line = bytes(file.stdout.readline()).decode("utf-8").strip()
                    print("." + line)
        except (InterruptedError, KeyboardInterrupt):
            log.warning("Polling process has been interrupted command='%s'", cmd_line)
        except subprocess.CalledProcessError as err:
            log.error("Command failed: %s => %s", cmd_line, err)
            syserr(str(err))

    @staticmethod
    def open(filename: str):
        """Open the specified file using the default editor."""
        my_os = os.environ.get("HHS_MY_OS", platform.system())
        if "Darwin" == my_os:
            Terminal.shell_exec(f"open {filename}")
        elif "Linux" == my_os:
            Terminal.shell_exec(f"xdg-open {filename}")
        else:
            raise Exception(f"OS '{my_os}' is not supported")

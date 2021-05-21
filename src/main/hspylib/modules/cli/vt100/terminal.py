#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.vt100
      @file: terminal.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import select
import shlex
import subprocess
from abc import ABC
from typing import Optional

from hspylib.core.tools.commons import syserr


class Terminal(ABC):
    
    @staticmethod
    def shell_exec(cmd_line: str, **kwargs) -> Optional[str]:
        try:
            log.info(f"Executing shell command: {cmd_line}")
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            result = subprocess.check_output(cmd_args, **kwargs).decode("utf-8")
            log.info(f"Execution result: {result}")
            return result.strip() if result else None
        except subprocess.CalledProcessError as err:
            log.error(f'Failed => {str(err)}')
            syserr(str(err))
            return None
    
    @staticmethod
    def shell_poll(cmd_line: str, **kwargs) -> None:
        if 'stdout' in kwargs:
            del kwargs['stdout']  # Deleted since we use our own
        if 'stdout' in kwargs:
            del kwargs['stderr']  # Deleted since we use our own
        try:
            log.info(f"Polling shell command: {cmd_line}")
            cmd_args = list(filter(None, shlex.split(cmd_line)))
            with(subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)) as file:
                process = select.poll()
                process.register(file.stdout)
                while True:
                    line = bytes(file.stdout.readline()).decode('utf-8').strip()
                    print('.' + line)
        except (InterruptedError, KeyboardInterrupt):
            log.warning(f"Polling process has been interrupted command='{cmd_line}'")
        except subprocess.CalledProcessError as err:
            log.debug(f'Failed => {str(err)}')
            syserr(str(err))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @Package: main.enums
      @file: exit_status.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration
from hspylib.modules.cli.vt100.vt_colors import VtColors


class ExitStatus(Enumeration):
    """The exit status of an executed command is the value returned by the waitpid system call or equivalent function.
    Exit statuses fall between 0 and 255, though, as explained below, the shell may use values above 125 specially.
    Exit statuses from shell builtins and compound commands are also limited to this range. Under certain circumstances,
    the shell will use special values to indicate specific failure modes."""

    # @formatter:off

    # Returned when something went wrong due to any Human interaction
    ERROR   = 129

    # Returned when something ran successfully without errors
    SUCCESS =  0

    # Returned when something that was supposed to work and failed due to unexpected software behaviour
    FAILED  =  62

    # Returned when something ran should be aborted. Generally due to usr cancellation
    ABORTED =  63

    # @formatter:on

    @staticmethod
    def of(value: int | type('ExitStatus')) -> 'ExitStatus':
        try:
            return value if isinstance(value, ExitStatus) else ExitStatus.of_value(value or 0)
        except TypeError:
            return ExitStatus.ERROR

    def __str__(self):
        return self.name

    def __repr__(self):
        color = VtColors.GREEN.code if self == ExitStatus.SUCCESS else VtColors.RED.code
        return f"{color}{self.name}({self.value}){VtColors.NC.code}"

    @property
    def val(self) -> int:
        return int(str(self.value))

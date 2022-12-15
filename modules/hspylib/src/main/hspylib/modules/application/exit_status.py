#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: hspylib.core.enums
      @file: exit_status.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration
from hspylib.modules.cli.vt100.vt_color import VtColor


class ExitStatus(Enumeration):
    """The exit status of an executed command is the value returned by the waitpid system call or equivalent function.
    Exit statuses fall between 0 and 255, though, as explained below, the shell may use values above 125 specially.
    Exit statuses from shell builtins and compound commands are also limited to this range. Under certain circumstances,
    the shell will use special values to indicate specific failure modes."""

    # fmt: off

    # Returned when something ran successfully without errors.
    NOT_SET     = None

    # Returned when something ran successfully without errors.
    SUCCESS     = 0

    # Returned when something went wrong due to any Human interaction.
    ERROR       = 1

    # Returned when something that was supposed to work and failed due to unexpected software behaviour.
    FAILED      = 2

    # Returned when something ran should be aborted. Generally due to user cancellation.
    ABORTED     = 127

    # Returned when something unexpected occurred.
    ABNORMAL    = 129

    # fmt: on

    @staticmethod
    def of(value: int | SystemExit) -> "ExitStatus":
        try:
            return ExitStatus.of_value(value.code if isinstance(value, SystemExit) else value or 0)
        except TypeError:
            return ExitStatus.ABNORMAL

    def __str__(self):
        return self.name

    def __repr__(self):
        color = VtColor.GREEN.code if self == ExitStatus.SUCCESS else VtColor.RED.code
        return f"{color}{self.name}({self.value}){VtColor.NC.code}"

    @property
    def val(self) -> int:
        return int(str(self.value))

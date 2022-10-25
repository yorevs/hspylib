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
    FAILED  =  1

    # Returned when something ran should be aborted. Generally due to usr cancellation
    ABORTED =  2

    # @formatter:on

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}{}({})".format(
            '\033[0;32m' if self.name == 'SUCCESS' else '\033[0;31m',
            self.name, self.value
        )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @Package: hspylib.main.hspylib.core.enums
      @file: exit_code.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class ExitCode(Enumeration):
    """TODO"""

    # @formatter:off

    # Returned when something went wrong due to any Human interaction
    ERROR = -1

    # Returned when something ran successfully without errors
    SUCCESS = 0

    # Returned when something that was supposed to work and failed due to unexpected software behaviour
    FAILED = 1

    # Additional exit codes can be defined here {
    # }

    # @formatter:on

    def __str__(self):
        return f"{self.name}({self.value})"

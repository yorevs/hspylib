#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.cfman.exception
      @file: exceptions.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.exception.exceptions import HSBaseException


class CFConnectionError(HSBaseException):
    """Raised when failed to connect to CloudFoundry"""


class CFExecutionError(HSBaseException):
    """Raised when failed to execute a cf command"""


class CFAuthenticationError(HSBaseException):
    """Raised when failed to authenticate to CloudFoundry"""

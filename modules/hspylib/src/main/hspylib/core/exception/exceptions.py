#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.exception
      @file: exceptions.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
import sys


class HSBaseException(Exception):
    """This is a generic exception and should not be raised. It may be inherited instead"""

    def __init__(self, message: str, cause: Exception = None):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_type and exc_obj and exc_tb:
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_cause = str(cause) if cause else ""
            fmt_msg = f"### {message} :{err_cause}: (File {filename}, Line {exc_tb.tb_lineno})"
        else:
            fmt_msg = message
        super().__init__(fmt_msg)
        log.error(fmt_msg)


class ApplicationError(HSBaseException):
    """Raised when the application filed to execute is not found"""


class InputAbortedError(HSBaseException):
    """Raised when an input method is aborted"""


class WidgetNotFoundError(HSBaseException):
    """Raised when widget is not found on any of the widget paths"""


class WidgetExecutionError(HSBaseException):
    """Raised when widget failed to execute"""


class KeyboardInputError(HSBaseException):
    """Raised when an invalid keystroke input is provided"""


class ResourceNotFoundError(HSBaseException):
    """Raised when resource path is not found"""


class SourceNotFoundError(HSBaseException):
    """Raised when source path is not found"""


class InvalidOptionError(HSBaseException):
    """Raised when an invalid option is received by the application"""


class InvalidInputError(Exception):
    """Raised when an invalid input is provided"""


class InvalidArgumentError(Exception):
    """Raised when an invalid argument is received by the application"""


class InvalidStateError(Exception):
    """Raised when an invalid state is detected by the application"""


class NotATerminalError(NotImplementedError):
    """Raised when a TTY terminal is required"""

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


class HSBaseException(Exception):
    """This is a generic exception and should not be raised. It may be inherited instead"""

    def __init__(self, message: str, cause: Exception = None):
        fmt_msg = f'{message}' + (' => {str(cause)}' if cause else '')
        super().__init__(fmt_msg)
        log.error(fmt_msg)


class EntityNotFoundError(HSBaseException):
    """Raised when an entity is not found"""


class InputAbortedError(HSBaseException):
    """Raised when an input method is aborted"""


class ProgrammingError(HSBaseException):
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""


class InvalidOptionError(HSBaseException):
    """Raised when an invalid option is received by the application"""


class NotConnectedError(HSBaseException):
    """Raised when an attempt to execute without being connected but a connection is required"""


class WidgetNotFoundError(HSBaseException):
    """Raised when widget is not found on any of the widget paths"""


class WidgetExecutionError(HSBaseException):
    """Raised when widget failed to execute"""


class KeyboardInputError(HSBaseException):
    """Raised when an invalid keystroke input is provided"""


class UnsupportedSchemaError(HSBaseException):
    """Raised when an invalid schema is provided """


class SchemaRegistryError(HSBaseException):
    """Raised when schema registration or API access fails"""


class InvalidInputError(Exception):
    """Raised when an invalid input is provided """


class InvalidArgumentError(Exception):
    """Raised when an invalid argument is received by the application"""


class InvalidStateError(Exception):
    """Raised when an invalid state is detected by the application"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: datasource.exception
      @file: exceptions.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.exception.exceptions import HSBaseException


class EntityNotFoundError(HSBaseException):
    """Raised when an entity is not found"""


class DatabaseConnectionError(HSBaseException):
    """Raised when all connection attempts to the database exhausted"""


class DatabaseError(HSBaseException):
    """Raised when database failed to execute/create-session"""


class ProgrammingError(HSBaseException):
    """Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc."""

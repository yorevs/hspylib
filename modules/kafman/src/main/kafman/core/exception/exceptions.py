#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.core.exception
      @file: exceptions.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.exception.exceptions import HSBaseException


class InvalidSchemaError(HSBaseException):
    """Raised when an invalid schema is provided"""


class SchemaRegistryError(HSBaseException):
    """Raised when schema registration or API access fails"""

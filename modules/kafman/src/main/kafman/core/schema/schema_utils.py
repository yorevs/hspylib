#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema
      @file: schema_utils.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HomeSetup team
"""

from abc import ABC
from typing import Any
from hspylib.core.exception.exceptions import InvalidStateError


class SchemaUtils(ABC):

    @staticmethod
    def check_and_get(
        attribute: str,
        content: dict = None,
        required: bool = True,
        default: Any = None) -> Any:

        if content and attribute in content:
            return content[attribute]
        else:
            if required:
                raise InvalidStateError(f'Required attribute {attribute} was not found in content string !')

        return default

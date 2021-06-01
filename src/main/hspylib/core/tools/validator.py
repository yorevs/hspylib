#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.tools
      @file: validator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Tuple, Type

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Validator(ABC):

    @staticmethod
    def assert_valid(errors: list, validation: Tuple[bool, str], throw_if_invalid: bool = False) -> None:
        if not validation[0]:
            if throw_if_invalid:
                raise AssertionError(validation[1])
            errors.append(validation[1])

    @staticmethod
    def is_not_blank(input_string: str, min_length: int = 0) -> bool:
        return input_string and len(input_string) >= min_length

    @staticmethod
    def matches(
            input_string: str,
            regex_pattern: str) -> bool:

        return bool(re.match(regex_pattern, input_string))

    @staticmethod
    def is_integer(
            number: str,
            min_value: int = 0,
            max_value: int = 65535) -> bool:

        return number.isdigit() and min_value <= int(number) <= max_value

    @staticmethod
    def is_float(
            number: str,
            min_value: float = 0,
            max_value: float = 65535) -> bool:

        return number.isdecimal() and min_value <= float(number) <= max_value

    @staticmethod
    def is_enum(
            name: str,
            enum_type: Type) -> bool:

        return name.upper() in enum_type.__dict__

    @staticmethod
    def is_date(
            date_text: str,
            fmt: str = DEFAULT_DATE_FORMAT) -> bool:

        try:
            datetime.strptime(date_text, fmt)
            return True
        except ValueError:
            return False

    @staticmethod
    def has_no_nulls(*args) -> bool:
        return all(opt is not None for opt in args)

    @abstractmethod
    def __call__(self, *args, **kwargs) -> bool:
        pass

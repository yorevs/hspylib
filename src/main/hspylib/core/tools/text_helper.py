#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.tools
      @file: text_helper.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import random
import re

from hspylib.core.tools.commons import get_or_default


def fit_text(text: str, width: int) -> str:
    return text if len(text) <= width else text[0:width - 3] + '...'


def rand_string(choices: str, length: int) -> str:
    return ''.join(random.choices(choices, k=length))


def justified_left(string: str, width: int, fill: str = ' ') -> str:
    return string.ljust(width, fill)


def justified_center(string: str, width: int, fill: str = ' ') -> str:
    return string.center(width, fill)


def justified_right(string: str, width: int, fill: str = ' ') -> str:
    return string.rjust(width, fill)


def uppercase(string: str) -> str:
    return string.upper()


def lowercase(string: str) -> str:
    return string.lower()


def camelcase(string: str) -> str:
    return string.capitalize()


def cut(string: str, index: int) -> str:
    result = tuple(re.split(r' +', string))
    return get_or_default(result, index)


class TextAlignment:
    """
    Table cell text justification helper.
    """
    LEFT = justified_left
    CENTER = justified_center
    RIGHT = justified_right


class TextCase:
    """
    Table cell text justification helper.
    """
    UPPER_CASE = uppercase
    LOWER_CASE = lowercase
    CAMEL_CASE = camelcase

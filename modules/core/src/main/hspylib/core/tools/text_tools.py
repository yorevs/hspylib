#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.core.tools
      @file: text_tools.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import random
import re
from abc import ABC

from hspylib.core.tools.commons import get_or_default


def fit_text(text: str, width: int) -> str:
    """TODO"""
    return text if len(text) <= width else text[0:width - 3] + '...'


def rand_string(choices: str, length: int) -> str:
    """TODO"""
    return ''.join(random.choices(choices, k=length))


def justified_left(string: str, width: int, fill: str = ' ') -> str:
    """TODO"""
    return string.ljust(width, fill)


def justified_center(string: str, width: int, fill: str = ' ') -> str:
    """TODO"""
    return string.center(width, fill)


def justified_right(string: str, width: int, fill: str = ' ') -> str:
    """TODO"""
    return string.rjust(width, fill)


def uppercase(string: str) -> str:
    """TODO"""
    return string.upper()


def lowercase(string: str) -> str:
    """TODO"""
    return string.lower()


def camelcase(string: str, separator: str = '_|-') -> str:
    """TODO"""
    parts = re.split(rf'{separator}+', string)
    return '_'.join([p.capitalize() for p in parts])


def snakecase(string: str) -> str:
    """TODO"""
    return string.strip().lower().replace(' ', '_').replace('-', '_')


def cut(string: str, index: int, separator: str = ' ') -> str:
    """TODO"""
    result = tuple(re.split(rf'{separator}+', string))
    return get_or_default(result, index)


def strip_escapes(string: str) -> str:
    """TODO"""
    return re.compile(r'\x1b[^m]*m').sub('', string)


# pylint: disable=too-few-public-methods
class TextAlignment(ABC):
    """
    Table cell text justification helper.
    """
    LEFT = justified_left
    CENTER = justified_center
    RIGHT = justified_right


# pylint: disable=too-few-public-methods
class TextCase(ABC):
    """
    Table cell text justification helper.
    """
    UPPER_CASE = uppercase
    LOWER_CASE = lowercase
    CAMEL_CASE = camelcase

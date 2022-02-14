#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   main.modules.cli.tui.extra.minput
      @file: input_validator.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
import typing


class InputValidator:
    """TODO"""

    RE_FMT_LETTER = r'^[a-zA-Z]{%min%,%max%}$'
    RE_FMT_WORD = r'^[a-zA-Z0-9 _]{%min%,%max%}$'
    RE_FMT_NUMBER = r'^[0-9\.]{%min%,%max%}$'
    RE_FMT_TOKEN = r'^\<?[a-zA-Z0-9_\- ]+\>?(\|\<?[a-zA-Z0-9_\- ]+\>?)*$'
    RE_FMT_MASKED = r'.*\|.+'
    RE_FMT_ANYTHING = r'^.{%min%,%max%}$'

    def __init__(self, min_length: int = 1, max_length: int = 30, pattern: str = None):
        self._min_length = min_length
        self._max_length = max_length
        self._pattern = pattern or self.RE_FMT_ANYTHING

    def __str__(self):
        return f"r\"{self._pattern}\""

    def __repr__(self):
        return str(self)

    @staticmethod
    def letters(min_length: int = 1, max_length: int = 30) -> typing.Any:
        return InputValidator(min_length, max_length, InputValidator.RE_FMT_LETTER)

    @staticmethod
    def words(min_length: int = 1, max_length: int = 30) -> typing.Any:
        return InputValidator(min_length, max_length, InputValidator.RE_FMT_WORD)

    @staticmethod
    def numbers(min_length: int = 1, max_length: int = 30) -> typing.Any:
        return InputValidator(min_length, max_length, InputValidator.RE_FMT_NUMBER)

    @staticmethod
    def anything(min_length: int = 1, max_length: int = 30) -> typing.Any:
        return InputValidator(min_length, max_length, InputValidator.RE_FMT_ANYTHING)

    @staticmethod
    def custom(pattern: str) -> typing.Any:
        return InputValidator(pattern=pattern)

    def validate(self, value: str) -> bool:
        regex = self._get_pattern()
        return re.search(regex, value) is not None

    def _get_pattern(self):
        return self._pattern \
            .replace('%min%', str(self._min_length or 1)) \
            .replace('%max%', str(self._max_length or 30))

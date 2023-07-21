#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.minput
      @file: input_validator.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.validator import Validator

import re


class InputValidator(Validator):
    """MenuInput 'input' validator."""

    class PatternType(Enumeration):
        # fmt: off
        CUSTOM      = r''  # It will be set later
        ANYTHING    = r'.'
        LETTERS     = r'[a-zA-Z]'
        WORDS       = r'[a-zA-Z0-9 _]'
        NUMBERS     = r'[0-9\.\,]'
        MASKED      = r'[a-zA-Z0-9]'
        # fmt: on

    @classmethod
    def custom(cls, pattern: str) -> "InputValidator":
        """Return a custom validator that allows customize the input rules.
        :param pattern: the custom validator pattern.
        """
        pattern_type = cls.PatternType.CUSTOM
        validator = InputValidator(pattern_type=pattern_type)
        validator.pattern = pattern
        return validator

    @classmethod
    def letters(cls) -> "InputValidator":
        """Return a validator that allows only letters."""
        return InputValidator(cls.PatternType.LETTERS)

    @classmethod
    def numbers(cls) -> "InputValidator":
        """Return a validator that allows only numbers."""
        return InputValidator(cls.PatternType.NUMBERS)

    @classmethod
    def words(cls) -> "InputValidator":
        """Return a validator that allows only words (space, numbers or letters)."""
        return InputValidator(cls.PatternType.WORDS)

    @classmethod
    def anything(cls) -> "InputValidator":
        """Return a validator that allows any input value."""
        return InputValidator(cls.PatternType.ANYTHING)

    @classmethod
    def masked(cls) -> "InputValidator":
        """Return a validator that allows masked inputs."""
        return InputValidator(cls.PatternType.MASKED)

    def __init__(self, pattern_type: PatternType = PatternType.ANYTHING):
        self._pattern_type = pattern_type
        self._pattern = pattern_type.value

    def __str__(self) -> str:
        return f'r"{self.pattern}"' if self.pattern_type == self.PatternType.CUSTOM else self.pattern_type.name

    def __repr__(self):
        return str(self)

    def __call__(self, *args, **kwargs) -> bool:
        return all(self.validate(value) for value in args)

    def validate(self, value: str) -> bool:
        """Validate the value against the validator pattern."""
        unmasked_value = re.split("[|,;]", value)[0] if value else ""
        return bool(re.match(self.pattern, unmasked_value))

    @property
    def pattern(self) -> str:
        return str(self._pattern)

    @pattern.setter
    def pattern(self, pattern: str) -> None:
        self._pattern = rf"{pattern}"

    @property
    def pattern_type(self) -> PatternType:
        return self._pattern_type

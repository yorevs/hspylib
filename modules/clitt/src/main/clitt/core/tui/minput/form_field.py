#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.minput
      @file: form_field.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any

from clitt.core.icons.font_awesome.form_icons import FormIcons
from clitt.core.tui.minput.access_type import AccessType
from clitt.core.tui.minput.input_type import InputType
from clitt.core.tui.minput.input_validator import InputValidator


class FormField:
    """TODO"""

    def __init__(
        self,
        label: str = None,
        dest: str = None,
        itype: InputType = InputType.TEXT,
        min_length: int = 0,
        max_length: int = 30,
        access_type: AccessType = AccessType.READ_WRITE,
        value: Any = "",
        validator: InputValidator = None,
    ):

        self.label = label
        self.dest = dest
        self.itype = itype
        self.min_length = min_length
        self.max_length = max_length
        self.access_type = access_type
        self.value = value
        self.validator = validator or InputValidator.anything(min_length, max_length)

    def __str__(self) -> str:
        return f"{self.label}: {self.itype}({self.min_length}-{self.max_length}) [{self.access_type}] = '{self.value}'"

    def __repr__(self):
        return str(self)

    @property
    def width(self) -> int:
        return len(str(self.value)) if self.itype != InputType.SELECT else 1

    @property
    def icon(self) -> FormIcons:
        if self.access_type == AccessType.READ_ONLY:
            return FormIcons.LOCKED
        match self.itype:
            case InputType.PASSWORD:
                icon = FormIcons.HIDDEN
            case InputType.CHECKBOX:
                icon = FormIcons.MARKED
            case InputType.SELECT:
                icon = FormIcons.SELECTABLE
            case InputType.MASKED:
                icon = FormIcons.MASKED
            case InputType.TEXT:
                if self.validator.pattern_type == InputValidator.PatternType.NUMBERS:
                    icon = FormIcons.NUMBERS
                elif self.validator.pattern_type == InputValidator.PatternType.LETTERS:
                    icon = FormIcons.LETTERS
                elif self.validator.pattern_type == InputValidator.PatternType.WORDS:
                    icon = FormIcons.EDITABLE
                else:
                    icon = FormIcons.EDITABLE
            case _:
                icon = FormIcons.QUESTION_CIRCLE
        return icon

    def can_write(self) -> bool:
        return self.access_type == AccessType.READ_WRITE

    def assign(self, value: Any) -> bool:
        if self.validate(value):
            self.value = value
            return True
        return False

    def validate(self, value: Any = None) -> bool:
        return self.validator.validate(str(value) or str(self.value)) if self.validator else False

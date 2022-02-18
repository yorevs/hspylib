#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.extra.minput
      @file: form_field.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any

from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.cli.tui.extra.minput.access_type import AccessType
from hspylib.modules.cli.tui.extra.minput.input_type import InputType
from hspylib.modules.cli.tui.extra.minput.input_validator import InputValidator


class FormField:
    """TODO"""

    def __init__(
        self,
        label: str = None,
        itype: InputType = InputType.TEXT,
        min_length: int = 0,
        max_length: int = 30,
        access_type: AccessType = AccessType.READ_WRITE,
        value: Any = '',
        validator: InputValidator = None):

        self.value = value
        self.label = label
        self.itype = itype
        self.min_length = min_length
        self.max_length = max_length
        self.access_type = access_type
        self.validator = validator or InputValidator.anything(min_length, max_length)
        self.icon = self.get_icon()

    def __str__(self) -> str:
        return f"{self.label}: {self.itype}({self.min_length}-{self.max_length}) [{self.access_type}] = '{self.value}'"

    def __repr__(self):
        return str(self)

    def get_icon(self) -> FormIcons:
        if self.access_type == AccessType.READ_ONLY:
            icon = FormIcons.LOCKED
        elif self.itype == InputType.PASSWORD:
            icon = FormIcons.HIDDEN
        elif self.itype == InputType.CHECKBOX:
            icon = FormIcons.MARKED
        elif self.itype == InputType.SELECT:
            icon = FormIcons.SELECTABLE
        elif self.itype == InputType.MASKED:
            icon = FormIcons.MASKED
        else:
            icon = FormIcons.EDITABLE

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

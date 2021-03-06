#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.cli.tui.extra.minput
      @file: field_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any

from hspylib.core.tools.text_tools import camelcase
from hspylib.modules.cli.tui.extra.minput.access_type import AccessType
from hspylib.modules.cli.tui.extra.minput.form_field import FormField
from hspylib.modules.cli.tui.extra.minput.input_type import InputType
from hspylib.modules.cli.tui.extra.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.extra.minput.minput_utils import MInputUtils


class FieldBuilder:

    def __init__(self, parent: Any):
        self.parent = parent
        self.field = FormField()

    def label(self, label: str) -> Any:
        self.field.label = label
        return self

    def itype(self, itype: str) -> Any:
        self.field.itype = InputType.of_value(itype)
        return self

    def validator(self, validator: InputValidator) -> Any:
        self.field.validator = validator
        return self

    def min_max_length(self, min_length: int, max_length: int) -> Any:
        assert max_length >= min_length, f"Not a valid field length: ({min_length}-{max_length})"
        assert max_length > 0 and min_length > 0, f"Not a valid field length: ({min_length}-{max_length})"
        self.field.min_length = min_length
        self.field.max_length = max_length
        return self

    def access_type(self, access_type: str) -> Any:
        self.field.access_type = AccessType.of_value(access_type)
        return self

    def value(self, value: Any) -> Any:
        assert self.field.assign(value), \
            f"Not a valid value: \"{value}\". Validation pattern=\"{self.field.validator}\""
        return self

    def build(self) -> Any:
        self.field.itype = self.field.itype or InputType.TEXT
        if self.field.itype == InputType.CHECKBOX:
            self.field.value = self.field.value if self.field.value in ['0', '1'] else 0
            self.field.min_length = self.field.max_length = 1
            self.validator(InputValidator.custom(r'[01]'))
        elif self.field.itype == InputType.SELECT:
            self.field.min_length = self.field.max_length = 1
            self.validator(InputValidator.anything())
        elif self.field.itype == InputType.MASKED:
            _, mask = MInputUtils.unpack_masked(self.field.value)
            self.field.min_length = self.field.max_length = len(mask)
            self.validator(InputValidator.custom(mask.replace('#', '[0-9]').replace('@', '[a-zA-Z]').replace('*', '.')))
        self.field.label = camelcase(self.field.label) or 'Field'
        self.field.min_length = self.field.min_length or 1
        self.field.max_length = self.field.max_length or 30
        self.field.access_type = self.field.access_type or AccessType.READ_WRITE
        self.field.icon = self.field.get_icon()
        self.field.value = self.field.value if self.field.value else ''
        self.parent.fields.append(self.field)
        return self.parent

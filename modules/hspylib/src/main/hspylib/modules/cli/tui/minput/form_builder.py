#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.tui.minput
      @file: form_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Any

from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import str_to_bool
from hspylib.core.tools.text_tools import snakecase
from hspylib.modules.cli.tui.minput.access_type import AccessType
from hspylib.modules.cli.tui.minput.form_field import FormField
from hspylib.modules.cli.tui.minput.input_type import InputType
from hspylib.modules.cli.tui.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.minput.minput_utils import MInputUtils


class FormBuilder:
    """TODO"""

    class FieldBuilder:
        """TODO"""

        def __init__(self, parent: Any):
            self.parent = parent
            self.field = FormField()

        def label(self, label: str) -> "FormBuilder.FieldBuilder":
            self.field.label = label
            return self

        def dest(self, dest: str) -> "FormBuilder.FieldBuilder":
            self.field.dest = dest
            return self

        def itype(self, itype: str) -> "FormBuilder.FieldBuilder":
            self.field.itype = InputType.of_value(itype)
            return self

        def validator(self, validator: InputValidator) -> "FormBuilder.FieldBuilder":
            self.field.validator = validator
            return self

        def min_max_length(self, min_length: int, max_length: int) -> "FormBuilder.FieldBuilder":
            check_argument(max_length >= min_length, "Not a valid field length: ({}-{})", min_length, max_length)
            check_argument(max_length > 0 and min_length > 0, "Not a valid field length: ({}-{})", min_length,
                           max_length)
            self.field.min_length = min_length
            self.field.max_length = max_length
            return self

        def access_type(self, access_type: str) -> "FormBuilder.FieldBuilder":
            self.field.access_type = AccessType.of_value(access_type)
            return self

        def value(self, value: Any | None) -> "FormBuilder.FieldBuilder":
            check_argument(
                not value or self.field.assign(value),
                'Not a valid value: "{}". Validation pattern="{}"', value, self.field.validator
            )
            return self

        def build(self) -> Any:
            self.field.itype = self.field.itype or InputType.TEXT
            if self.field.itype == InputType.CHECKBOX:
                self.field.value = "1" if str_to_bool(str(self.field.value)) else "0"
                self.field.min_length = self.field.max_length = 1
                self.validator(InputValidator.custom(r"[01]"))
            elif self.field.itype == InputType.SELECT:
                self.field.min_length = self.field.max_length = 1
                self.validator(InputValidator.anything())
            elif self.field.itype == InputType.MASKED:
                _, mask = MInputUtils.unpack_masked(self.field.value)
                self.field.min_length = self.field.max_length = len(mask)
                # fmt: off
                self.validator(
                    InputValidator.custom(
                        mask
                        .replace("#", "[0-9]")
                        .replace("@", "[a-zA-Z]")
                        .replace("*", ".")
                    ))
                # fmt: on
            self.field.label = self.field.label or "Field"
            self.field.dest = self.field.dest or f"{snakecase(self.field.label)}"
            self.field.min_length = self.field.min_length or 1
            self.field.max_length = self.field.max_length or 30
            self.field.access_type = self.field.access_type or AccessType.READ_WRITE
            self.field.value = self.field.value if self.field.value else ""
            self.parent.fields.append(self.field)
            return self.parent

    def __init__(self) -> None:
        self.fields = []

    def field(self) -> Any:
        return FormBuilder.FieldBuilder(self)

    def build(self) -> list:
        return self.fields

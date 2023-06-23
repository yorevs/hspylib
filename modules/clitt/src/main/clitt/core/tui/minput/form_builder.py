#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.minput
      @file: form_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import re
from typing import Any, List

from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import str_to_bool
from hspylib.core.tools.dict_tools import get_or_default
from hspylib.core.tools.text_tools import snakecase

from clitt.core.tui.minput.access_type import AccessType
from clitt.core.tui.minput.form_field import FormField
from clitt.core.tui.minput.input_type import InputType
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.minput_utils import unpack_masked


class FormBuilder:
    """MenuInput form builder."""

    @staticmethod
    def or_else_get(options: tuple | list, index: int, default_value: Any = None) -> Any:
        """TODO"""
        return get_or_default(options, index, default_value) or default_value

    class FieldBuilder:
        """MenuInput form field builder."""

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
            self.field.input_validator = validator
            return self

        def min_max_length(self, min_length: int, max_length: int) -> "FormBuilder.FieldBuilder":
            check_argument(max_length >= min_length, "Not a valid field length: ({}-{})", min_length, max_length)
            check_argument(
                max_length > 0 and min_length > 0, "Not a valid field length: ({}-{})", min_length, max_length
            )
            self.field.min_length = min_length
            self.field.max_length = max_length
            return self

        def access_type(self, access_type: str) -> "FormBuilder.FieldBuilder":
            self.field.access_type = AccessType.of_value(access_type)
            return self

        def value(self, value: Any | None) -> "FormBuilder.FieldBuilder":
            check_argument(
                not value or self.field.assign(value, True),
                'Not a valid value: "{}". Validation pattern="{}"',
                value,
                self.field.input_validator,
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
                _, mask = unpack_masked(self.field.value)
                self.field.min_length = self.field.max_length = len(mask)
                self.validator(
                    InputValidator.custom(
                        mask
                        .replace("#", "[0-9]")
                        .replace("@", "[a-zA-Z]")
                        .replace("%", "[a-zA-Z0-9]")
                        .replace("*", ".")
                    ))
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

    def from_tokenized(self, tokenized_fields: List[str]) -> 'FormBuilder':
        """Construct the forms based on string tokens.

         Field tokens (in-order):
              <Label> : The field label. Consisting only of alphanumeric characters and under‐scores.
               [Mode] : The input mode. One of {[text]|password|checkbox|select}.
               [Type] : The input type. One of {letters|numbers|words|[anything]}.
        [Min/Max len] : The minimum and maximum length of characters allowed. Defaults to [0/30].
               [Perm] : The field permissions. One of {r|[rw]}. Where \"r\" for Read Only ; \"rw\" for Read & Write.
              [Value] : The initial value of the field. This field may not be blank if the field is read only.
        """
        for tk_field in tokenized_fields:
            parts = list(map(str.strip, tk_field.split('|')))
            validator_fn = getattr(InputValidator, self.or_else_get(parts, 2, 'anything'))
            min_max = list(map(int, map(str.strip, self.or_else_get(parts, 3, '1/30').split('/'))))
            access = re.sub('^rw$', 'read-write', self.or_else_get(parts, 4, 'rw'))
            access = re.sub('^r$', 'read-only', access)
            # fmt: off
            self.field() \
                .label(self.or_else_get(parts, 0, 'Label')) \
                .itype(self.or_else_get(parts, 1, 'text')) \
                .min_max_length(
                    self.or_else_get(min_max, 0, 1),
                    self.or_else_get(min_max, 1, 30)
                ) \
                .access_type(access) \
                .validator(validator_fn()) \
                .value(self.or_else_get(parts, 5, None)) \
                .build()
            # fmt: on

        return self

    def field(self) -> Any:
        return FormBuilder.FieldBuilder(self)

    def build(self) -> list:
        return self.fields

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
from clitt.core.tui.minput.field_builder import FieldBuilder
from clitt.core.tui.minput.form_field import FormField
from clitt.core.tui.minput.input_validator import InputValidator
from hspylib.core.tools.dict_tools import get_or_default
from typing import Any, List

import re


class FormBuilder:
    """MenuInput form builder."""

    def __init__(self) -> None:
        self.fields = []
        self._fn_validate = None

    @staticmethod
    def get_attr(parts: List[str], index: int, default_value: Any = None) -> str:
        return get_or_default(parts, index, default_value) or default_value

    def from_tokenized(self, minput_tokens: List[str], separator: chr = "|") -> "FormBuilder":
        """Construct the forms based on string tokens.

         Field tokens (in-order):
              <Label> : The field label. Consisting only of alphanumeric characters and under‐scores.
               [Mode] : The input mode. One of {[text]|password|checkbox|select}.
               [Type] : The input type. One of {letters|numbers|words|[anything]}.
        [Min/Max len] : The minimum and maximum length of characters allowed. Defaults to [0/30].
               [Perm] : The field permissions. One of {r|[rw]}. Where \"r\" for Read Only ; \"rw\" for Read & Write.
              [Value] : The initial value of the field. This field may not be blank if the field is read only.
        """
        for tk_field in minput_tokens:
            parts = list(map(str.strip, tk_field.split(separator)))
            validator_fn = getattr(InputValidator, self.get_attr(parts, 2, "anything"))
            min_max = list(map(int, map(str.strip, self.get_attr(parts, 3, "5/30").split("/"))))
            access = re.sub("^rw$", "read-write", self.get_attr(parts, 4, "rw"))
            access = re.sub("^r$", "read-only", access)
            # fmt: off
            self.field() \
                .label(self.get_attr(parts, 0, 'Label')) \
                .itype(self.get_attr(parts, 1, 'text')) \
                .min_max_length(
                    get_or_default(min_max, 0, 5),
                    get_or_default(min_max, 1, 30)
                ) \
                .access_type(access) \
                .validator(validator_fn()) \
                .value(self.get_attr(parts, 5, None)) \
                .build()
            # fmt: on

        return self

    def field(self) -> Any:
        return FieldBuilder(self)

    def build(self) -> List[FormField]:
        return self.fields

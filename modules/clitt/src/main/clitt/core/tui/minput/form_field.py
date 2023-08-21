#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.minput
      @file: form_field.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.form_icons import FormIcons
from clitt.core.tui.minput.access_type import AccessType
from clitt.core.tui.minput.input_type import InputType
from clitt.core.tui.minput.input_validator import InputValidator
from clitt.core.tui.minput.minput_utils import get_selected, MASK_SYMBOLS, toggle_selected, unpack_masked
from hspylib.core.exception.exceptions import InvalidInputError
from hspylib.core.tools.text_tools import xstr
from typing import Any, Callable, Optional, TypeAlias

FieldValidator_Fn: TypeAlias = Callable[["FormField"], bool]


class FormField:
    """Represent a MenuInput form field."""

    def __init__(
        self,
        label: str = None,
        dest: str = None,
        itype: InputType = InputType.TEXT,
        min_length: int = 5,
        max_length: int = 30,
        access_type: AccessType = AccessType.READ_WRITE,
        value: Any = "",
        input_validator: InputValidator = InputValidator.anything(),
        field_validator: FieldValidator_Fn = None,
        tooltip: str = None,
    ):
        self._label = label
        self._tooltip = tooltip
        self._dest = dest
        self._itype = itype
        self._min_length = min_length
        self._max_length = max_length
        self._access_type = access_type
        self.input_validator = input_validator
        self.field_validator = field_validator
        self._value = self.assign(value)

    def __str__(self) -> str:
        return (
            f"[{self.label}, {self.itype.name}({self.min_length}/{self.max_length})"
            f"<{self.access_type}> = '{self.value or ''}']"
        )

    def __repr__(self):
        return str(self)

    @property
    def label(self) -> str:
        return self._label

    @property
    def tooltip(self) -> str:
        return self._tooltip

    @property
    def dest(self) -> str:
        return self._dest

    @property
    def itype(self) -> InputType:
        return self._itype

    @property
    def min_length(self) -> int:
        return self._min_length

    @property
    def max_length(self) -> int:
        return self._max_length

    @property
    def access_type(self) -> AccessType:
        return self._access_type

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        self._value = self.assign(new_value)

    @property
    def length(self) -> int:
        """Get the field real length, depending on the field type."""
        real_value = str(self.value or "")
        match self.itype:
            case InputType.CHECKBOX:
                real_value = "1"
            case InputType.SELECT:
                _, real_value = get_selected(str(self.value))
            case InputType.MASKED:
                real_value, mask = unpack_masked(str(self.value))
                idx = len(real_value)
                while idx < len(mask) and mask[idx] not in MASK_SYMBOLS:
                    idx += 1
                return idx

        return len(real_value)

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
                if self.input_validator.pattern_type == InputValidator.PatternType.NUMBERS:
                    icon = FormIcons.NUMBERS
                elif self.input_validator.pattern_type == InputValidator.PatternType.LETTERS:
                    icon = FormIcons.LETTERS
                elif self.input_validator.pattern_type == InputValidator.PatternType.WORDS:
                    icon = FormIcons.WORDS
                elif self.input_validator.pattern_type == InputValidator.PatternType.CUSTOM:
                    icon = FormIcons.CUSTOM
                else:
                    icon = FormIcons.EDITABLE
            case _:
                icon = FormIcons.QUESTION_CIRCLE
        return icon

    def can_write(self) -> bool:
        """Whether this field value can be set or not."""
        return self.access_type == AccessType.READ_WRITE

    def assign(self, value: Any) -> Any:
        """Assign a value for this field. Must match the input validator, otherwise an exception will be thrown.
        :param value: TODO
        """
        valid = True
        if value is not None and self.input_validator:
            match self.itype:
                case InputType.MASKED:
                    unpack_masked(value)
                case InputType.SELECT:
                    toggle_selected(value)
                case InputType.CHECKBOX:
                    valid = isinstance(value, bool)
                case _:
                    valid = all(self.validate_input(val) for val in xstr(value))

        if not valid:
            raise InvalidInputError(f"Value {value} is invalid!")

        self._value = value

        return self._value

    def validate_input(self, value: Any = None) -> bool:
        """Validate the input using the assigned validator.
        :param value: the value to validate against.
        """
        return self.input_validator(str(value)) if self.input_validator else True

    def validate_field(self) -> bool:
        """Validate the field using the assigned validator function."""
        return self.field_validator(self) if self.field_validator else False

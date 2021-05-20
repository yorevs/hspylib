#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra.minput
      @file: form_field.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any

from hspylib.modules.cli.menu.extra.minput.access_type import AccessType
from hspylib.modules.cli.menu.extra.minput.input_type import InputType
from hspylib.modules.cli.menu.extra.minput.input_validator import InputValidator


class FormField:
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

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    def can_write(self) -> bool:
        return self.access_type == AccessType.READ_WRITE

    def assign(self, value: Any) -> bool:
        if self.validate(value):
            self.value = value
            return True

        return False

    def validate(self, value: Any = None) -> bool:
        return self.validator.validate(str(value) or str(self.value)) if self.validator else False

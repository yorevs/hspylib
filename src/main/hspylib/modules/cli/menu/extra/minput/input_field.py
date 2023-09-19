#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra.minput
      @file: input_field.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any


class InputField:
    def __init__(
            self,
            label: str = None,
            mode: str = 'input',
            kind: str = 'any',
            min_length: int = 0,
            max_length: int = 30,
            access_type: str = 'read-write',
            value: Any = None):

        self.label = label
        self.mode = mode
        self.kind = kind
        self.min_length = min_length
        self.max_length = max_length
        self.access_type = access_type
        self.value = value

    def __str__(self) -> str:
        return str(self.__dict__)

    def can_write(self) -> bool:
        return self.access_type == 'read-write'

    def val_regex(self, min_length: int, max_length: int) -> str:
        if self.kind == 'letter':
            regex = r'^[a-zA-Z]{' + str(min_length) + ',' + str(max_length) + '}$'
        elif self.kind == 'number':
            regex = r'^[0-9]{' + str(min_length) + ',' + str(max_length) + '}$'
        elif self.kind == 'word':
            regex = r'^[a-zA-Z0-9 _]{' + str(min_length) + ',' + str(max_length) + '}$'
        elif self.kind == 'token':
            regex = r'\<?[a-zA-Z0-9_\- ]+\>?(\|\<?[a-zA-Z0-9_\- ]+\>?)*'
        else:
            regex = r'.{' + str(min_length) + ',' + str(max_length) + '}$'

        return regex

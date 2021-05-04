#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.application
      @file: argument.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re
from typing import Any


class Argument:

    def __init__(self, arg_name: str, validation_regex: str = '.*', required: bool = True, next_in_chain: Any = None):
        self.arg_name = arg_name
        self.validation_regex = validation_regex
        self.required = required
        self.next_in_chain = next_in_chain
        self.value = ''

    def __str__(self):
        return "arg_nam: {}, validation_regex: {}, required: {}, value: {}, next: {}" \
            .format(self.arg_name, self.validation_regex, self.required, self.value, self.next_in_chain)

    def __repr__(self):
        return str(self)

    def set_value(self, provided_arg: str) -> bool:
        self.value = provided_arg if re.match(rf'^({self.validation_regex})$', provided_arg) else None
        return True if self.value else False

    def set_next(self, argument: Any) -> None:
        self.next_in_chain = argument

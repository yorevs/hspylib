#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.cli.tui.extra.minput
      @file: form_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any

from hspylib.modules.cli.tui.extra.minput.field_builder import FieldBuilder


class FormBuilder:
    def __init__(self):
        self.fields = []

    def field(self) -> Any:
        return FieldBuilder(self)

    def build(self) -> list:
        return self.fields

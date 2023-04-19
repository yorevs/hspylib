#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.core.schema.json.property
      @file: enum_property.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils
from PyQt5.QtWidgets import QWidget
from typing import List


class EnumProperty(SchemaField):
    def __init__(self, name: str, description: str, symbols: List[str], default: str, required: bool = True):
        super().__init__(name, description, JsonType.ENUM, default, required)

        self.symbols = symbols

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget_type(self.a_type.value)()
        return WidgetUtils.setup_combo_box(self.widget, self.symbols, self.doc)

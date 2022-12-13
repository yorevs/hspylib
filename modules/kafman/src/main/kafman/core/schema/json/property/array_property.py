#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.json.property
      @file: array_property.py
   @created: Fri, 1 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from kafman.core.schema.json.json_type import JsonType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils
from PyQt5.QtWidgets import QWidget
from typing import List


class ArrayProperty(SchemaField):
    def __init__(self, name: str, description: str, a_items: List[str], required: bool = True):
        super().__init__(name, description, JsonType.ARRAY, required=required)

        self.a_items = a_items

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget_type(self.a_type.value)()
        return WidgetUtils.setup_list(self.widget, self.a_items, self.doc)

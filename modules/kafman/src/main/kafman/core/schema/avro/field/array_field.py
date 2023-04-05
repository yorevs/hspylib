#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman.core.schema.avro.field
      @file: array_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import List

from PyQt5.QtWidgets import QWidget

from kafman.core.schema.avro.avro_type import AvroType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils


class ArrayField(SchemaField):
    def __init__(self, name: str, doc: str, items: List[str], default: str = None, required: bool = True):
        super().__init__(name, doc, AvroType.ARRAY, default, required=required)

        self.items = items

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget_type(self.a_type.value)()
        return WidgetUtils.setup_widget(self.widget, self.doc, self.items, default=self.default)

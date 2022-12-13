#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.field
      @file: enum_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.modules.qt.promotions.hcombobox import HComboBox
from kafman.core.schema.avro.avro_type import AvroType
from kafman.core.schema.schema_field import SchemaField
from kafman.core.schema.widget_utils import WidgetUtils
from PyQt5.QtWidgets import QWidget
from typing import List


class EnumField(SchemaField):
    def __init__(self, name: str, doc: str, symbols: List[str], default: str = None, required: bool = True):
        super().__init__(name, doc, AvroType.ENUM, default, required=required)

        self.symbols = symbols

    def create_input_widget(self) -> QWidget:
        self.widget: HComboBox = WidgetUtils.get_widget_type(self.a_type.value)()
        return WidgetUtils.setup_combo_box(self.widget, self.symbols, self.doc, default=self.default)

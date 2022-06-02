#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.core.schema.field
      @file: array_field.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HomeSetup team
"""

from typing import List, Optional
from PyQt5.QtWidgets import QWidget
from kafman.core.schema.field.schema_field import SchemaField
from kafman.core.schema.field.schema_field_type import SchemaFieldType
from kafman.core.schema.widget_utils import WidgetUtils



class ArrayField(SchemaField):

    def __init__(
        self,
        name: str,
        doc: str,
        items: List[str],
        default: str = None,
        required: bool = True):

        super().__init__(
            name,
            doc,
            SchemaFieldType.ARRAY,
            default,
            required=required)

        self.items = items

    def create_input_widget(self) -> QWidget:
        self.widget = WidgetUtils.get_widget_type(self.a_type)()
        return WidgetUtils.setup_widget(self.widget, self.doc, self.items, default=self.default)

    def get_value(self) -> Optional[dict]:
        pass

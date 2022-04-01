#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
      @file: schema_field.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any, List, Optional, Tuple

from hspylib.core.tools.commons import new_dynamic_object
from hspylib.core.tools.preconditions import check_not_none
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from PyQt5.QtWidgets import QAbstractSpinBox, QCheckBox, QLabel, QLineEdit, QStackedWidget, QWidget

from kafman.core.schema.schema_field_type import SchemaFieldType
from kafman.core.schema.widget_utils import WidgetUtils


class SchemaField:
    """Represents a schema registry field and form component.
        - Avro Types: https://avro.apache.org/docs/current/spec.html#schema_record
        - Json Types: https://json-schema.org/understanding-json-schema/reference/type.html
    """

    @staticmethod
    def of_complex(
        name: str, doc: str, complex_types: dict,  default: Any = None, required: bool = True) -> 'SchemaField':
        return SchemaField(
            name, doc, SchemaFieldType.COMPLEX, default, field_complex_types=complex_types, required=required)

    @staticmethod
    def of_primitive(
        name: str, doc: str, primitive_type: SchemaFieldType, default: Any = None,
        required: bool = True) -> 'SchemaField':
        return SchemaField(name, doc, primitive_type, default, required=required)

    @staticmethod
    def of_fixed(name: str, doc: str, size: int) -> 'SchemaField':
        return SchemaField(name, doc, SchemaFieldType.FIXED, field_default=size)

    @staticmethod
    def of_record(name: str, doc: str, required: bool = True) -> 'SchemaField':
        return SchemaField(name, doc, SchemaFieldType.RECORD, required=required)

    @staticmethod
    def of_enum(name: str, doc: str, symbols: List[str], default: str = None, required: bool = True) -> 'SchemaField':
        return SchemaField(name, doc, SchemaFieldType.ENUM, default, field_symbols=symbols, required=required)

    @staticmethod
    def of_array(name: str, doc: str, items: List[Any], default: str = None, required: bool = True) -> 'SchemaField':
        return SchemaField(name, doc, SchemaFieldType.ARRAY, default, field_items=items, required=required)

    @staticmethod
    def of_map(name: str, doc: str, values: dict, default: str = None, required: bool = True) -> 'SchemaField':
        return SchemaField(name, doc, SchemaFieldType.MAP, default, field_values=values, required=required)

    def __init__(
        self,
        field_name: str,
        field_doc: str,
        field_type: SchemaFieldType,
        field_default: Any = None,
        field_fields: list = None,
        field_symbols: List[str] = None,
        field_items: list = None,
        field_values: dict = None,
        field_complex_types: dict = None,
        required: bool = True):

        self._field_name = field_name
        self._field_doc = field_doc
        self._field_type = field_type
        self._field_default = field_default
        self._field_attributes = new_dynamic_object('SchemaFieldAttributes')
        self._field_attributes.fields = field_fields
        self._field_attributes.symbols = field_symbols
        self._field_attributes.items = field_items
        self._field_attributes.values = field_values
        self._field_attributes.complex_types = field_complex_types
        self._required = required
        self._form_widget = None

    def __str__(self):
        return \
            f"name={self._field_name}, " \
            f"type={str(self._field_type)}, " \
            f"required={self._required}, "

    def create_form_row_widgets(
        self,
        stack_widget: QStackedWidget) -> Tuple[QLabel, QLabel, QWidget]:
        """TODO"""

        self._form_widget = stack_widget
        label = QLabel(f"{self.get_name()[0].upper() + self.get_name()[1:]}: ")
        if self.is_required():
            req_label = QLabel('*')
            req_label.setStyleSheet('QLabel {color: #FF554D;}')
        else:
            req_label = QLabel(' ')
        req_label.setToolTip(f"This field is {'required' if self.is_required() else 'optional'}")
        widget = WidgetUtils.create_input_widget(
            self._field_type,
            self._field_attributes.complex_types,
            self._field_doc,
            self._field_default)
        if not self.is_complex_type():
            WidgetUtils.setup_widget(
                widget,
                self._field_doc,
                self._field_attributes.symbols,
                self._field_default,
            )

        return req_label, label, widget

    def get_name(self) -> str:
        """Return the name of the field"""
        return self._field_name

    def get_avro_type(self) -> SchemaFieldType:
        """Return the avro type of the field"""
        return self._field_type

    def is_required(self) -> bool:
        """Whether the field is required or optional"""
        return self._required

    def is_valid(self, widget: QWidget) -> bool:
        """Whether the field is valid, based on it's values and required flag"""
        return not self.is_required() or self.get_value(widget) is not None

    def is_complex_type(self) -> bool:
        """Whether the field is a complex type"""
        return self._field_attributes.complex_types is not None

    def get_value(self, widget: QWidget) -> Optional[dict]:
        """Return the value contained by the schema widget. This may vary depending on the QWidget class"""
        check_not_none(widget)
        value = None
        if isinstance(widget, QAbstractSpinBox):
            value = widget.value()
        elif isinstance(widget, QCheckBox):
            value = bool(widget.isChecked())
        elif isinstance(widget, HComboBox):
            current_text = widget.currentText()
            value = [current_text] if self._field_type == 'array' else current_text
        elif isinstance(widget, QLineEdit):
            value = widget.text()

        return {self._field_name: value} if value else None

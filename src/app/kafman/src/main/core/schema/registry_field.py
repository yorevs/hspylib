#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: registry_field.py
   @created: Thu, 5 Aug 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Union, Type, Optional, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, QWidget, QSizePolicy, QAbstractSpinBox

from hspylib.core.tools.commons import get_by_key_or_default
from hspylib.core.tools.preconditions import check_not_none
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from kafman.src.main.core.schema.kafka_schema import KafkaSchema


class RegistryField:
    """Represents a schema registry field and form component.
        - Avro Types: https://avro.apache.org/docs/current/spec.html#schema_record
        - Json Types: https://json-schema.org/understanding-json-schema/reference/type.html
    """

    QWIDGET_TYPE_MAP = {
        'int': QSpinBox,
        'integer': QSpinBox,
        'long': QSpinBox,
        'float': QDoubleSpinBox,
        'double': QDoubleSpinBox,
        'number': QDoubleSpinBox,
        'boolean': QCheckBox,
        'string': QLineEdit,
        'bytes': QLineEdit,
        'array': HComboBox,
        'enum': HComboBox,
    }

    @staticmethod
    def of(
        schema: KafkaSchema,
        field_name: str,
        field_type: str,
        field_attrs: dict,
        required: bool = True) -> 'RegistryField':
        """Construct a RegistryField from a the field attributes"""

        return RegistryField(
            schema,
            field_name,
            field_type,
            required,
            field_attrs
        )

    def __init__(
        self,
        schema: KafkaSchema,
        name: str,
        field_type: Union[str, list],
        required: bool,
        field_attrs: dict):

        self._schema = schema
        self._name = name
        self._type = next((typ for typ in field_type if typ != 'null'), None) \
            if isinstance(field_type, list) \
            else field_type
        self._required = required
        self._field_attrs = field_attrs
        self._widget_type = self._widget_type()

    def __str__(self):
        return f"name={self._name}, type={self._type}, required={self._required}, widget={self._widget_type.__class__}"

    def get_value(self, widget_instance: QWidget) -> Optional[dict]:
        """TODO"""
        check_not_none(widget_instance)
        if isinstance(widget_instance, QAbstractSpinBox):
            value = widget_instance.value()
        elif isinstance(widget_instance, QCheckBox):
            value = bool(widget_instance.isChecked())
        elif isinstance(widget_instance, HComboBox):
            current_text = widget_instance.currentText()
            value = [current_text] if self._type == 'array' else current_text
        else:
            value = widget_instance.text()

        return {self._name: value} if value else None

    def get_name(self) -> str:
        """TODO"""
        return self._name

    def get_type(self) -> Union[str, list]:
        """TODO"""
        return self._type

    def is_required(self) -> bool:
        """TODO"""
        return self._required

    def is_valid(self, widget_instance: QWidget) -> bool:
        """TODO"""
        return not self.is_required() or self.get_value(widget_instance) is not None

    def widget(self) -> QWidget:
        """TODO"""
        widget_instance = self._widget_type()
        default_value = get_by_key_or_default(self._field_attrs, 'default', '')
        placeholder_text = self._placeholder_text()
        tooltip = get_by_key_or_default(self._field_attrs, 'examples')
        tooltip = ('Examples: \n' + '\n'.join([f'  - {str(t)}' for t in tooltip])) \
            if tooltip \
            else placeholder_text
        if self._widget_type == HComboBox:
            items = self._schema.array_items(self._field_attrs)
            widget_instance.addItems(items)
            widget_instance.setEditable(True)
            widget_instance.lineEdit().setPlaceholderText(placeholder_text)
            widget_instance.setCurrentText(default_value or widget_instance.itemText(0))
            widget_instance.setLayoutDirection(Qt.RightToLeft)
        elif self._widget_type == QCheckBox:
            widget_instance.setChecked(bool(default_value))
        elif self._widget_type in [QSpinBox, QDoubleSpinBox]:
            min_val, max_val = self._min_max_values()
            widget_instance.setMinimum(min_val)
            widget_instance.setMaximum(max_val)
            widget_instance.setValue(default_value or 0)
        else:
            widget_instance.setPlaceholderText(placeholder_text)
            widget_instance.setText(str(default_value))
        widget_instance.setToolTip(tooltip)
        widget_instance.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return widget_instance

    def _widget_type(self) -> Type[QWidget]:
        """TODO"""
        return self.QWIDGET_TYPE_MAP[self._type] \
            if self._type in self.QWIDGET_TYPE_MAP \
            else QLineEdit

    def _placeholder_text(self) -> str:
        """TODO"""
        text = get_by_key_or_default(self._field_attrs, 'description')
        text = get_by_key_or_default(self._field_attrs, 'doc') if not text else text
        text = f"This field is {'required' if self._required else 'optional'}" if not text else text
        return text

    def _min_max_values(self) -> Tuple[Union[int, float], Union[int, float]]:
        """TODO"""
        min_val = get_by_key_or_default(self._field_attrs, 'minimum', 0)
        max_val = get_by_key_or_default(
            self._field_attrs, 'maximum', 99999.99
            if self._widget_type() == QDoubleSpinBox
            else 99999)
        return min_val, max_val

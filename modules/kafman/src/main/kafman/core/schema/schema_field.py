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

from typing import Any, Optional, Tuple, Type, Union

from hspylib.core.tools.commons import get_by_key_or_default
from hspylib.core.tools.preconditions import check_not_none
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractSpinBox, QCheckBox, QDoubleSpinBox, QLabel, QLineEdit, QPushButton, QSizePolicy, \
    QSpinBox, \
    QWidget


class SchemaField:
    """Represents a schema registry field and form component.
        - Avro Types: https://avro.apache.org/docs/current/spec.html#schema_record
        - Json Types: https://json-schema.org/understanding-json-schema/reference/type.html
    """

    QWIDGET_TYPE_MAP = {
        'boolean': QCheckBox,
        'integer': QSpinBox,
        'int': QSpinBox,
        'long': QSpinBox,
        'float': QDoubleSpinBox,
        'double': QDoubleSpinBox,
        'number': QDoubleSpinBox,
        'bytes': QLineEdit,
        'string': QLineEdit,
        'fixed': QLineEdit,
        'enum': HComboBox,
        'array': HComboBox,
        'record': QPushButton,
        'object': QPushButton
    }

    @staticmethod
    def of(
        field_name: str,
        field_type: str,
        field_attrs: dict,
        field_symbols: list = None,
        required: bool = True) -> 'SchemaField':
        """Construct a RegistryField from the schema field properties"""

        return SchemaField(
            field_name,
            field_type,
            field_attrs,
            field_symbols,
            required,
        )

    def __init__(
        self,
        field_name: str,
        field_type: Any,
        field_attrs: dict,
        field_symbols: list,
        required: bool):

        self._field_name = field_name
        self._field_type = field_type
        self._field_attrs = field_attrs
        self._field_symbols = field_symbols
        self._required = required
        self._widget_type = self._get_widget_type()

    def __str__(self):
        return f"name={self._field_name}, type={self._field_type}, required={self._required}, widget={self._widget_type.__class__}"

    def get_value(self, widget: QWidget) -> Optional[dict]:
        """Return the value contained by the schema widget. This may vary depending on the QWidget class"""
        check_not_none(widget)
        if isinstance(widget, QAbstractSpinBox):
            value = widget.value()
        elif isinstance(widget, QCheckBox):
            value = bool(widget.isChecked())
        elif isinstance(widget, HComboBox):
            current_text = widget.currentText()
            value = [current_text] if self._field_type == 'array' else current_text
        else:
            value = widget.text()

        return {self._field_name: value} if value else None

    def get_name(self) -> str:
        """Return the name of the field"""
        return self._field_name

    def get_type(self) -> Union[str, list]:
        """Return the type of the field"""
        return self._field_type

    def is_required(self) -> bool:
        """Whether the field is required or optional"""
        return self._required

    def is_valid(self, widget: QWidget) -> bool:
        """Whether the field is valid, based on it's values and required flag"""
        return not self.is_required() or self.get_value(widget) is not None

    def get_widget(self) -> QWidget:
        """Return the QWidget that the field is displayed at the schema form"""
        widget = self._widget_type()
        default_value = get_by_key_or_default(self._field_attrs, 'default', '')
        placeholder_text = self._get_placeholder_text()
        tooltip = get_by_key_or_default(self._field_attrs, 'examples')
        tooltip = ('Examples: \n' + '\n'.join([f'  - {str(t)}' for t in tooltip])) \
            if tooltip \
            else placeholder_text
        if self._widget_type == HComboBox:
            widget.addItems(self._field_symbols)
            widget.setEditable(True)
            widget.lineEdit().setPlaceholderText(placeholder_text)
            widget.setCurrentText(default_value or widget.itemText(0))
        elif self._widget_type == QCheckBox:
            widget.setChecked(bool(default_value))
        elif self._widget_type in [QSpinBox, QDoubleSpinBox]:
            min_val, max_val = self._get_min_max_values()
            widget.setMinimum(min_val)
            widget.setMaximum(max_val)
            widget.setValue(default_value or 0)
            widget.setLayoutDirection(Qt.RightToLeft)
        else:
            widget.setPlaceholderText(placeholder_text)
            widget.setText(str(default_value or ''))
        widget.setToolTip(tooltip)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        return widget

    def _get_widget_type(self) -> Type[QWidget]:
        """Return the QWidget type required by this field"""
        return self.QWIDGET_TYPE_MAP[self._field_type] \
            if self._field_type in self.QWIDGET_TYPE_MAP \
            else QLabel

    def _get_placeholder_text(self) -> str:
        """Return the placeholder text to be displayed by this field"""
        text = get_by_key_or_default(self._field_attrs, 'description')
        text = get_by_key_or_default(self._field_attrs, 'doc') if not text else text
        text = f"This field is {'required' if self._required else 'optional'}" if not text else text
        return text

    def _get_min_max_values(self) -> Tuple[Union[int, float], Union[int, float]]:
        """Return the minimum and maximum numbers tha this field is allowed to hold"""
        min_val = get_by_key_or_default(self._field_attrs, 'minimum', 0)
        max_val = get_by_key_or_default(
            self._field_attrs, 'maximum', 99999.99
            if self._widget_type() == QDoubleSpinBox
            else 99999)
        return min_val, max_val

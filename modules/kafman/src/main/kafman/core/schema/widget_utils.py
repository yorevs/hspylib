#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman.core.schema
      @file: widget_utils.py
   @created: Wed, 1 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC
from typing import List, TypeVar, Union

from hspylib.core.exception.exceptions import InvalidStateError
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from hspylib.modules.qt.promotions.hlistwidget import HListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QLineEdit, QSizePolicy, QSpinBox, QToolButton, QWidget

INPUT_WIDGET = TypeVar(
    "INPUT_WIDGET", QWidget, HComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QToolButton, QCheckBox, HListWidget
)

INPUT_VALUE = TypeVar("INPUT_VALUE", int, str, bool, float, list)


class WidgetUtils(ABC):
    QWIDGET_TYPE_MAP = {
        "boolean": QCheckBox,
        "integer": QSpinBox,
        "int": QSpinBox,
        "long": QSpinBox,
        "float": QDoubleSpinBox,
        "double": QDoubleSpinBox,
        "number": QDoubleSpinBox,
        "bytes": QLineEdit,
        "string": QLineEdit,
        "fixed": QLineEdit,
        "enum": HComboBox,
        "array": HListWidget,
        "record": None,
        "object": None,
    }

    @staticmethod
    def get_widget_type(field_type: str) -> INPUT_WIDGET:
        return WidgetUtils.QWIDGET_TYPE_MAP[field_type]

    @staticmethod
    def setup_widget(
        widget: INPUT_WIDGET, doc: str = None, symbols: list = None, default: Union[str, int, float, bool] = None
    ) -> QWidget:
        """Return the QWidget that the field is displayed at the schema form"""

        widget_type = widget.__class__
        tooltip = doc
        if widget_type == HComboBox:
            WidgetUtils.setup_combo_box(widget, symbols, tooltip, default)
        elif widget_type == HListWidget:
            WidgetUtils.setup_list(widget, tooltip, default)
        elif widget_type == QCheckBox:
            WidgetUtils.setup_checkbox(widget, tooltip, default)
        elif widget_type == QSpinBox:
            WidgetUtils.setup_spin_box(widget, tooltip, default)
        elif widget_type == QDoubleSpinBox:
            WidgetUtils.setup_double_spin_box(widget, tooltip, default)
        elif widget_type == QLineEdit:
            WidgetUtils.setup_line_edit(widget, tooltip)
        else:
            raise InvalidStateError(f'Widget type "{widget_type.name}" is not supported')

        return widget

    @staticmethod
    def setup_widget_commons(widget: QWidget, tooltip: str) -> QWidget:
        widget.setToolTip(tooltip)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        widget.setStyleSheet("QWidget {padding: 5px;}")
        widget.setFont(QFont("DroidSansMono Nerd Font", 14))
        widget.setMinimumHeight(35)

        return widget

    @staticmethod
    def setup_combo_box(widget: HComboBox, symbols: List[str], tooltip: str = None, default: str = None) -> QWidget:

        widget.addItems(symbols or default or [])
        widget.setEditable(True)
        widget.lineEdit().setPlaceholderText(tooltip)
        widget.setCurrentText(default or widget.itemText(0))

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_list(widget: HListWidget, tooltip: str = None, all_items: List[str] = None) -> QWidget:

        list(map(widget.set_item, all_items or []))
        widget.set_editable()
        widget.set_selectable()
        widget.set_context_menu_enable()

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_checkbox(widget: QCheckBox, tooltip: str = None, default: Union[int, float] = False) -> QWidget:

        widget.setChecked(default or False)

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_spin_box(widget: QSpinBox, tooltip: str = None, default: int = 0) -> QWidget:

        min_val, max_val = 0, 9999
        widget.setMinimum(min_val)
        widget.setMaximum(max_val)
        widget.setValue(default or 0)
        widget.setLayoutDirection(Qt.RightToLeft)

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_double_spin_box(widget: QDoubleSpinBox, tooltip: str = None, default: float = 0.0) -> QWidget:

        min_val, max_val = 0.0, 9999.9999
        widget.setMinimum(min_val)
        widget.setMaximum(max_val)
        widget.setValue(default or 0)
        widget.setLayoutDirection(Qt.RightToLeft)

        return WidgetUtils.setup_widget_commons(widget, tooltip)

    @staticmethod
    def setup_line_edit(widget: QLineEdit, tooltip: str = None, default: str = "") -> QWidget:

        widget.setPlaceholderText(tooltip)
        widget.setText(default or "")

        return WidgetUtils.setup_widget_commons(widget, tooltip)

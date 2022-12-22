#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Kafman
   @package: kafman.views.promotions
      @file: form_pane.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from collections import defaultdict
from typing import Optional

from hspylib.core.preconditions import check_argument, check_not_none
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from hspylib.modules.qt.promotions.hcombobox import HComboBox
from hspylib.modules.qt.promotions.hframe import HFrame
from hspylib.modules.qt.promotions.hlistwidget import HListWidget
from hspylib.modules.qt.promotions.hstacked_widget import HStackedWidget
from PyQt5.QtWidgets import (
    QCheckBox, QDoubleSpinBox, QFrame, QGridLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QWidget,
)

from kafman.core.schema.widget_utils import INPUT_VALUE, INPUT_WIDGET, WidgetUtils
from kafman.views.promotions.form_area import FormArea


class FormPane(HFrame):
    """TODO"""

    LABEL_COLUMN = 0

    REQUIRED_COLUMN = 1

    FIELD_COLUMN = 2

    INPUT_WIDGETS = ["HComboBox", "HListWidget", "QCheckBox", "QSpinBox", "QDoubleSpinBox", "QLineEdit"]

    _forms = defaultdict()

    @staticmethod
    def _field_value(widget: INPUT_WIDGET) -> Optional[INPUT_VALUE]:
        """TODO"""

        widget_type = widget.__class__
        if widget_type == HComboBox:
            value = widget.currentText()
        elif widget_type == HListWidget:
            value = widget.as_list()
        elif widget_type == QCheckBox:
            value = widget.isChecked()
        elif widget_type in [QSpinBox, QDoubleSpinBox]:
            value = widget.value()
        elif widget_type == QLineEdit:
            value = widget.text()
        else:
            value = None

        return value

    def __init__(self, parent: QWidget, parent_form: "FormPane", form_name: str):
        super().__init__(parent)
        check_argument(form_name is not None and len(form_name) > 1, f"Invalid form name: {form_name}")
        self._fields = defaultdict()
        self._forms[form_name] = self
        self._name = form_name
        self._parent_form = parent_form
        self._form_frame = QFrame(self)
        self._form_area = FormArea(self)
        self._box = QVBoxLayout(self)
        self._grid = QGridLayout(self._form_frame)

        self.setObjectName(form_name)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self._box.addWidget(self._form_area)
        self._form_frame.setFrameStyle(QFrame.NoFrame)
        self._form_frame.setContentsMargins(0, 0, 0, 0)
        self._form_area.setWidget(self._form_frame)

    def __getitem__(self, form_name):
        return self._forms[form_name]

    def grid(self) -> QGridLayout:
        return self._grid

    def name(self) -> str:
        return self._name

    def parent_name(self) -> Optional[str]:
        return self._parent_form.name() if self._parent_form else None

    def add_field(self, field_name: str, label: QLabel, req_label: QLabel, widget: INPUT_WIDGET, row: int) -> None:
        """TODO"""

        check_not_none(widget)
        widget.setObjectName(field_name)
        self._grid.addWidget(label, row, self.LABEL_COLUMN)
        self._grid.addWidget(req_label, row, self.REQUIRED_COLUMN)
        self._grid.addWidget(widget, row, self.FIELD_COLUMN)
        self._fields[widget.objectName()] = defaultdict()

    def add_form_button(
        self, field_name: str, label: QLabel, req_label: QLabel, row: int, index: int, form_stack: HStackedWidget
    ) -> None:
        """TODO"""

        fill_button = QPushButton(FormIcons.ARROW_RIGHT.value + " Fill")
        fill_button.clicked.connect(lambda: form_stack.slide_to_index(index))
        WidgetUtils.setup_widget_commons(fill_button, "Click to fill the form")
        fill_button.setMaximumWidth(100)
        fill_button.setMinimumHeight(30)
        fill_button.setDefault(False)
        fill_button.setAutoDefault(False)
        self.add_field(field_name, label, req_label, fill_button, row)

    def add_back_button(self, back_index: int, form_stack: HStackedWidget) -> None:
        """TODO"""

        row = self._grid.rowCount() + 1
        back_button = QPushButton(FormIcons.ARROW_LEFT.value + " Back")
        back_button.clicked.connect(lambda: form_stack.slide_to_index(back_index))
        WidgetUtils.setup_widget_commons(back_button, "Click to go to previous form")
        back_button.setMaximumWidth(100)
        back_button.setMinimumHeight(30)
        back_button.setDefault(False)
        back_button.setAutoDefault(False)
        self._grid.addWidget(back_button, row, self.LABEL_COLUMN)

    def fields(self) -> dict:
        """TODO"""

        # update all field values
        for row in range(0, self._grid.rowCount()):
            item = self._grid.itemAtPosition(row, self.FIELD_COLUMN)
            widget = item.widget() if item else None
            if self._is_input_widget(widget):
                self._fields[widget.objectName()] = self._field_value(widget)

        return self._fields

    def _is_input_widget(self, widget: QWidget) -> bool:
        return widget is not None and type(widget).__name__ in self.INPUT_WIDGETS

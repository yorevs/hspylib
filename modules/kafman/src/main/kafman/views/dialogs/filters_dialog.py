#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib-kafman
   @package: hspylib-kafman.main.kafman.views.promotions
      @file: settings_dialog.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import random
import string
from typing import Optional, Union

from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.collection_filter import CollectionFilter, ElementFilter, FilterCondition
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialogButtonBox, QWidget

from kafman.__classpath__ import _Classpath


class FiltersDialog(QObject):
    """TODO"""

    filtersChanged = pyqtSignal(str)

    DIALOG_FORM = _Classpath.get_resource_path("forms/filters_dlg.ui")

    def __init__(self, parent: QWidget, filters: CollectionFilter):
        super().__init__(parent)
        ui_class, base_class = uic.loadUiType(self.DIALOG_FORM)
        check_not_none((ui_class, base_class))
        self.dialog, self.ui = base_class(parent), ui_class()
        self.ui.setupUi(self.dialog)
        self._filters = filters
        self._lookup = {}
        self._setup_controls()

    def _setup_controls(self) -> None:
        """TODO"""
        self.filtersChanged.connect(self._sync_filters)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setModal(True)
        self._set_font()
        self.ui.le_filter_value.setPlaceholderText('Type in the filter value')
        self.ui.btn_box.button(QDialogButtonBox.Discard).setText("Remove")
        self.ui.btn_box.clicked.connect(self._button_clicked)
        self.ui.tbtn_clear_filters.setText(FormIcons.CLEAR.value)
        self.ui.tbtn_clear_filters.clicked.connect(self._clear_filters)
        self.ui.cmb_filter_field.currentTextChanged.connect(self._field_changed)
        self.ui.cmb_filter_field.setCurrentText('value')
        self.ui.cmb_filter_condition.setCurrentText('contains')
        self._sync_filters()

    def _set_font(self) -> None:
        """TODO"""
        widgets = list(filter(lambda o: hasattr(getattr(self.ui, o), 'setFont'), vars(self.ui)))
        list(map(lambda w: getattr(self.ui, w).setFont(QFont("DroidSansMono Nerd Font", 13)), widgets))

    def show(self):
        """TODO"""
        self.dialog.exec()

    def _button_clicked(self, button) -> None:
        """TODO"""
        role = self.ui.btn_box.buttonRole(button)
        if role == QDialogButtonBox.ApplyRole:
            self._apply_filter()
        elif role == QDialogButtonBox.DestructiveRole:
            self._discard_filter()

    def _field_changed(self, el_name: str) -> None:
        self.ui.cmb_filter_condition.clear()
        if el_name in ['timestamp', 'partition', 'offset']:
            self.ui.cmb_filter_condition.addItems([
                str(FilterCondition.LESS_THAN), str(FilterCondition.LESS_THAN_OR_EQUALS_TO),
                str(FilterCondition.GREATER_THAN), str(FilterCondition.GREATER_THAN_OR_EQUALS_TO),
                str(FilterCondition.EQUALS_TO), str(FilterCondition.DIFFERENT_FROM)
            ])
        else:
            self.ui.cmb_filter_condition.addItems([
                str(FilterCondition.EQUALS_TO), str(FilterCondition.DIFFERENT_FROM),
                str(FilterCondition.CONTAINS), str(FilterCondition.DOES_NOT_CONTAIN)
            ])

    def _clear_filters(self) -> None:
        """TODO"""
        self._filters.clear()
        self._sync_filters()
        self.filtersChanged.emit(str(self._filters))

    def _sync_filters(self) -> None:
        """TODO"""
        self.ui.lst_filters.clear()
        list(map(self._add_filter, self._filters))

    def _add_filter(self, f: ElementFilter) -> None:
        """TODO"""
        self.ui.lst_filters.set_item(str(f))
        self._lookup[str(f)] = f.name

    def _apply_filter(self) -> None:
        """TODO"""
        el_name = self.ui.cmb_filter_field.currentText()
        el_value = self._get_filter_value(el_name)
        if el_value:
            condition = FilterCondition.value_of(self.ui.cmb_filter_condition.currentText().upper().replace(' ', '_'))
            name = f"F:{el_name}:{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
            self._filters.apply_filter(name, el_name, condition, el_value)
            self.filtersChanged.emit(str(self._filters))
            self.ui.le_filter_value.setText('')

    def _discard_filter(self) -> None:
        """TODO"""
        item = self.ui.lst_filters.currentItem()
        if item:
            self._filters.discard(self._lookup[str(item.text())])
            self.filtersChanged.emit(str(self._filters))

    def _get_filter_value(self, el_name: str) -> Optional[Union[str, int, float, bool]]:
        """TODO"""
        str_value = self.ui.le_filter_value.text()
        try:
            if el_name in ['timestamp', 'partition', 'offset']:
                return int(str_value)
        except TypeError:
            pass
        return str_value

import random
import string
from pathlib import Path
from typing import Optional, Union

from hspylib.core.tools.collection_filter import CollectionFilter, ElementFilter, FilterConditions
from hspylib.core.tools.commons import run_dir
from hspylib.modules.cli.icons.font_awesome.form_icons import FormIcons
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialogButtonBox, QWidget


class FiltersDialog(QObject):
    """TODO"""

    filtersChanged = pyqtSignal(str)

    DIALOG_FORM = str(Path(run_dir()) / "resources/forms/filters_dlg.ui")

    def __init__(self, parent: QWidget, filters: CollectionFilter):
        super().__init__(parent)
        ui_class, base_class = uic.loadUiType(self.DIALOG_FORM)
        assert ui_class is not None and base_class is not None
        self.dialog, self.ui = base_class(parent), ui_class()
        self.ui.setupUi(self.dialog)
        self.filters = filters
        self.lookup = {}
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
                str(FilterConditions.LESS_THAN), str(FilterConditions.LESS_THAN_OR_EQUALS_TO),
                str(FilterConditions.GREATER_THAN), str(FilterConditions.GREATER_THAN_OR_EQUALS_TO),
                str(FilterConditions.EQUALS_TO), str(FilterConditions.DIFFERENT_FROM)
            ])
        else:
            self.ui.cmb_filter_condition.addItems([
                str(FilterConditions.EQUALS_TO), str(FilterConditions.DIFFERENT_FROM),
                str(FilterConditions.CONTAINS), str(FilterConditions.DOES_NOT_CONTAIN)
            ])

    def _clear_filters(self) -> None:
        """TODO"""
        self.filters.clear()
        self._sync_filters()
        self.filtersChanged.emit(str(self.filters))

    def _sync_filters(self) -> None:
        """TODO"""
        self.ui.lst_filters.clear()
        list(map(lambda f: self._add_filter(f), self.filters))

    def _add_filter(self, f: ElementFilter) -> None:
        """TODO"""
        self.ui.lst_filters.set_item(str(f))
        self.lookup[str(f)] = f.name

    def _apply_filter(self) -> None:
        """TODO"""
        el_name = self.ui.cmb_filter_field.currentText()
        el_value = self._get_filter_value(el_name)
        if el_value:
            condition = FilterConditions.value_of(self.ui.cmb_filter_condition.currentText().upper().replace(' ', '_'))
            name = f"F:{el_name}:{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
            self.filters.apply_filter(name, el_name, condition, el_value)
            self.filtersChanged.emit(str(self.filters))
            self.ui.le_filter_value.setText('')

    def _discard_filter(self) -> None:
        """TODO"""
        item = self.ui.lst_filters.currentItem()
        if item:
            self.filters.discard(self.lookup[str(item.text())])
            self.filtersChanged.emit(str(self.filters))

    def _get_filter_value(self, el_name: str) -> Optional[Union[str, int, float, bool]]:
        """TODO"""
        str_value = self.ui.le_filter_value.text()
        try:
            if el_name in ['timestamp', 'partition', 'offset']:
                return int(str_value)
        except TypeError:
            pass
        return str_value

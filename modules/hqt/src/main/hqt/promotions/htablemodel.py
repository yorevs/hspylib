#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Hqt
   @package: hqt.promotions
      @file: htablemodel.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.collection_filter import CollectionFilter, FilterCondition
from hspylib.core.tools.commons import class_attribute_names, class_attribute_values
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QTableView
from typing import List, Tuple, Type, TypeVar, Union

import collections

T = TypeVar("T")


class HTableModel(QAbstractTableModel):
    """TODO"""

    def __init__(
        self,
        parent: QTableView,
        clazz: Type,
        headers: List[str] = None,
        table_data: List[T] = None,
        cell_alignments: List[Qt.AlignmentFlag] = None,
        max_rows: int = 500,
    ):
        QAbstractTableModel.__init__(self, parent)
        self._parent = parent
        self._clazz = clazz
        self._data = collections.deque(maxlen=max_rows)
        self._filters = CollectionFilter()
        self._headers = headers or self._headers_by_entity()
        self._cell_alignments = cell_alignments
        self._parent.setModel(self)
        self.push_data(table_data or [])

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:  # pylint: disable=unused-argument
        """TODO"""
        if 0 <= row < len(self._data):
            self.beginRemoveRows(QModelIndex(), row, row + 1)
            del self._data[row]
            self.layoutChanged.emit()
            self.endRemoveRows()
            return True
        return False

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        """TODO"""
        if role == Qt.DisplayRole:
            row_dict = self._data[index.row()].__dict__
            value = class_attribute_values(row_dict)[index.column()]
            ret_val = QVariant(str(value if value is not None else ""))
        elif role == Qt.TextAlignmentRole:
            ret_val = (
                QVariant(self._cell_alignments[index.column()])
                if self._cell_alignments
                else QVariant(Qt.AlignLeft | Qt.AlignVCenter)
            )
        elif role == Qt.BackgroundColorRole:
            light_gray = self._parent.palette().color(QPalette.Window).lighter(100)
            ret_val = QVariant(light_gray if index.row() % 2 != 0 else "")
        else:
            ret_val = None

        return ret_val or QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> QVariant:
        """TODO"""
        ret_val = None
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            ret_val = QVariant(self._headers[section].upper()) if len(self._headers) >= section else QVariant("-")
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            ret_val = QVariant(str(section))

        return ret_val if ret_val else QVariant()

    def rowCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self._data) if self._data else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self._headers) if self._data else 0

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        """TODO"""
        keys = class_attribute_names(self._clazz)
        self._data = sorted(self._data, key=lambda x: getattr(x, keys[column]), reverse=bool(order))
        self.layoutChanged.emit()

    def append(self, data: T):
        """TODO"""
        if data and not self._filters.should_filter(data):
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + 1)
            self._data.append(data)
            self.endInsertRows()
            self.layoutChanged.emit()

    def apply_filter(
        self, name: str, el_name: str, condition: FilterCondition, el_value: Union[int, str, bool, float]
    ) -> None:
        """TODO"""
        self._filters.apply_filter(name, el_name, condition, el_value)

    def filter(self) -> None:
        """TODO"""
        self._data = self._filters.filter(list(self._data))

    def row(self, index: QModelIndex) -> T:
        """TODO"""
        return self._data[index.row()]

    def column(self, index: QModelIndex) -> T:
        """TODO"""
        row = self.row(index)
        col_name = str(list(vars(row))[index.column()])
        return getattr(row, col_name)

    def push_data(self, data: Union[List[T], T]) -> None:
        """TODO"""
        if data:
            if isinstance(data, list):
                list(map(self.append, data))
            else:
                self.append(data)
            self.layoutChanged.emit()

    def clear(self):
        """TODO"""
        self._data.clear()
        self.layoutChanged.emit()

    def is_empty(self) -> bool:
        """TODO"""
        return len(self._data) == 0

    def refresh_data(self) -> None:
        """TODO"""
        self._data = self._filters.filter(list(self._data))
        self.layoutChanged.emit()

    def remove_rows(self, rows: List[QModelIndex]):
        """TODO"""
        # Because we are using deque, we need to sort DESC to avoid deleting wrong indexes
        for row in sorted(rows, reverse=True):
            self.removeRow(row.row())

    def _headers_by_entity(self) -> List[str]:
        """TODO"""
        attributes = class_attribute_names(self._clazz)
        return [str(x).capitalize() for x in attributes]

    def selected_data(self) -> Tuple[List[QModelIndex], List[T]]:
        """TODO"""
        sel_model = self._parent.selectionModel()
        if sel_model:
            sel_indexes = sel_model.selectedIndexes()
            sel_rows = {[idx.row() for idx in sel_indexes]}
            return sel_indexes, [self._data[row] for row in sel_rows]
        return [], []

    def filters(self) -> CollectionFilter:
        """TODO"""
        return self._filters

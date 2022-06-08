#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.qt.promotions
      @file: htablemodel.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import collections
from typing import List, Tuple, Type, TypeVar, Union

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QTableView

from hspylib.core.tools.collection_filter import CollectionFilter
from hspylib.core.tools.commons import class_attribute_names, class_attribute_values

T = TypeVar('T')


class HTableModel(QAbstractTableModel):
    """TODO"""

    def __init__(
        self,
        parent: QTableView,
        clazz: Type,
        headers: List[str] = None,
        table_data: List[T] = None,
        cell_alignments: List[Qt.AlignmentFlag] = None,
        max_rows: int = 500):

        QAbstractTableModel.__init__(self, parent)
        self.parent = parent
        self.clazz = clazz
        self.table_data = collections.deque(maxlen=max_rows)
        self.filtered_data = None
        self.filters = CollectionFilter()
        self.headers = headers or self._headers_by_entity()
        self.cell_alignments = cell_alignments
        self.parent.setModel(self)
        self.push_data(table_data or [])
        # self.layoutChanged.connect(self._filter_data)

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:  # pylint: disable=unused-argument
        """TODO"""
        if 0 <= row < len(self.table_data):
            del self.table_data[row]
            self.layoutChanged.emit()
            return True
        return False

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        """TODO"""
        keys = class_attribute_names(self.clazz)
        self.table_data = sorted(self._display_data(), key=lambda x: getattr(x, keys[column]), reverse=bool(order))
        self.layoutChanged.emit()

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        """TODO"""
        if role == Qt.DisplayRole:
            row_dict = self._display_data()[index.row()].__dict__
            value = class_attribute_values(row_dict)[index.column()]
            ret_val = QVariant(str(value if value is not None else ''))
        elif role == Qt.TextAlignmentRole:
            ret_val = QVariant(self.cell_alignments[index.column()]) \
                if self.cell_alignments else QVariant(Qt.AlignLeft | Qt.AlignVCenter)
        elif role == Qt.BackgroundColorRole:
            light_gray = self.parent.palette().color(QPalette.Window).lighter(100)
            ret_val = QVariant(light_gray if index.row() % 2 != 0 else '')
        else:
            ret_val = None

        return ret_val or QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> QVariant:
        """TODO"""
        ret_val = None
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            ret_val = QVariant(self.headers[section].upper()) \
                if len(self.headers) >= section else QVariant('-')
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            ret_val = QVariant(str(section))

        return ret_val if ret_val else QVariant()

    def rowCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self._display_data()) if self._display_data() else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self.headers) if self.headers else 0

    def row(self, index: QModelIndex) -> T:
        """TODO"""
        return self._display_data()[index.row()]

    def column(self, index: QModelIndex) -> T:
        """TODO"""
        row = self.row(index)
        col_name = str(list(vars(row))[index.column()])
        return getattr(row, col_name)

    def push_data(self, data: Union[List[T], T]) -> None:
        """TODO"""
        if data:
            if isinstance(data, list):
                list(map(self.table_data.append, data))
            else:
                self.table_data.append(data)
            self.layoutChanged.emit()

    def clear(self):
        """TODO"""
        self.table_data.clear()
        self.layoutChanged.emit()

    def selected_rows(self) -> Tuple[List[QModelIndex], List[T]]:
        """TODO"""
        model = self.parent.selectionModel()
        rows = model.selectedRows() if model else []
        return rows, [self._display_data()[r.row()] for r in rows] if model else []

    def remove_rows(self, rows: List[QModelIndex]):
        """TODO"""
        rows.sort(reverse=True)  # Because we are using deque, we need to sort DESC to avoid deleting wrong indexes
        for row in rows:
            self.removeRow(row.row())

    def _headers_by_entity(self) -> List[str]:
        """TODO"""
        attributes = class_attribute_names(self.clazz)
        return [str(x).capitalize() for x in attributes]

    def _display_data(self) -> collections.deque:
        """TODO"""
        return self.table_data

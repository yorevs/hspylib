#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.qt.promotions
      @file: htablemodel.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import collections
import logging as log
from typing import Type, List, TypeVar

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableView

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
        max_rows: int = 1000):

        QAbstractTableModel.__init__(self, parent)
        self.clazz = clazz
        self.table_data = collections.deque(maxlen=max_rows)
        list(map(self.table_data.append, table_data or []))
        self.headers = headers or self._headers_by_entity()
        self.cell_alignments = cell_alignments
        parent.setModel(self)
        log.info('{} table_headers={}'.format(clazz.__class__.__name__, '|'.join(self.headers)))

    def row(self, index: QModelIndex) -> T:
        """TODO"""
        return self.table_data[index.row()]

    def column(self, index: QModelIndex) -> T:
        """TODO"""
        return class_attribute_values(self.table_data[index.row()].__dict__)[index.column()]

    def push_data(self, data: List[T]):
        """TODO"""
        list(map(self.table_data.append, data))
        self.layoutChanged.emit()

    def clear(self):
        """TODO"""
        self.table_data.clear()
        self.layoutChanged.emit()

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        """TODO"""
        keys = class_attribute_names(self.clazz)
        self.table_data = sorted(self.table_data, key=lambda x: getattr(x, keys[column]), reverse=bool(order))
        self.layoutChanged.emit()

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        """TODO"""
        ret_val = QVariant()
        entity = class_attribute_values(self.table_data[index.row()].__dict__)[index.column()]
        str_entity = str(entity) if entity is not None else ''
        if role == Qt.DisplayRole:
            ret_val = \
                QVariant(str_entity)
        if role == Qt.TextAlignmentRole:
            ret_val = \
                QVariant(self.cell_alignments[index.column()]) \
                    if self.cell_alignments else QVariant(Qt.AlignLeft | Qt.AlignVCenter)
        if role == Qt.BackgroundColorRole:
            ret_val = \
                QVariant(QColor(57, 57, 57) if index.row() % 2 == 0 else '')

        return ret_val

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> QVariant:
        """TODO"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[section].upper()) if len(self.headers) >= section else QVariant('-')
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return QVariant(str(section))
        return QVariant()

    def rowCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self.table_data) if self.table_data and len(self.table_data) > 0 else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self.table_data[0].__dict__.keys()) if self.table_data and len(self.table_data) > 0 else 0

    def _headers_by_entity(self) -> List[str]:
        """TODO"""
        attributes = class_attribute_names(self.clazz)
        return [str(x).capitalize() for x in attributes]

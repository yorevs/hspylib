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
from typing import Any, Type, List, Optional

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableView

from hspylib.core.tools.commons import class_attribute_names, class_attribute_values


class HTableModel(QAbstractTableModel):
    """TODO"""

    def __init__(
        self,
        parent: Optional[QTableView],
        clazz: Type,
        headers: List[str] = None,
        table_data: List[Any] = None,
        cell_alignments: List[Qt.AlignmentFlag] = None,
        max_rows: int = 1000):

        QAbstractTableModel.__init__(self, parent)
        self.clazz = clazz
        self.table_data = collections.deque(maxlen=max_rows)
        list(map(self.table_data.append, table_data or []))
        self.headers = headers or self.headers_by_entity()
        self.cell_alignments = cell_alignments
        log.info('{} table_headers={}'.format(clazz.__class__.__name__, '|'.join(self.headers)))
        parent.setModel(self)

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

    def headers_by_entity(self) -> tuple:
        """TODO"""
        try:
            return class_attribute_names(self.clazz)
        except TypeError:
            raise TypeError('Default values required for entity header names')

    def rowCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self.table_data) if self.table_data and len(self.table_data) > 0 else 0

    def columnCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        """TODO"""
        return len(self.table_data[0].__dict__.keys()) if self.table_data and len(self.table_data) > 0 else 0

    def row(self, index: QModelIndex) -> Any:
        """TODO"""
        return self.table_data[index.row()]

    def push_data(self, data: List[Any]):
        """TODO"""
        for item in data:
            self.table_data.append(item)
        self.layoutChanged.emit()

    def clear(self):
        """TODO"""
        self.table_data.clear()
        self.layoutChanged.emit()

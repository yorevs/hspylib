#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt.promotions
      @file: entity_table_model.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
from typing import Any, Type

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableView

from hspylib.core.tools.commons import class_attribute_names, class_attribute_values


class DefaultTableModel(QAbstractTableModel):
    def __init__(self, clazz: Type, headers: list = None, cell_alignments: list = None, table_data: list = None,
                 parent: QTableView = None):
        QAbstractTableModel.__init__(self, parent)
        self.clazz = clazz
        self.table_data = table_data or []
        self.headers = headers or self.headers_by_entity()
        self.cell_alignments = cell_alignments or []
        log.info('{} table_headers={}'.format(clazz.__class__.__name__, '|'.join(self.headers)))
    
    def data(self, index: QModelIndex, role: int = ...) -> Any:
        entity = class_attribute_values(self.table_data[index.row()].__dict__)[index.column()]
        str_entity = str(entity) if entity else ''
        if role == Qt.DisplayRole:
            return str_entity
        if role == Qt.TextAlignmentRole:
            return self.cell_alignments[index.column()] if self.cell_alignments else Qt.AlignLeft
        if role == Qt.BackgroundColorRole:
            return QVariant() if entity else QColor(230, 230, 230)
        
        return QVariant()
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section].upper() if len(self.headers) >= section else '-'
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section
        return QVariant()
    
    def headers_by_entity(self) -> tuple:
        return class_attribute_names(self.clazz)
    
    def rowCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        return len(self.table_data) if self.table_data and len(self.table_data) > 0 else 0
    
    def columnCount(self, parent: QModelIndex = ...) -> int:  # pylint: disable=unused-argument
        return len(self.table_data[0].__dict__.keys()) if self.table_data and len(self.table_data) > 0 else 0
    
    def row(self, index: QModelIndex) -> Any:
        return self.table_data[index.row()]

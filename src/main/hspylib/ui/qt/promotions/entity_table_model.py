from typing import Type

from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableView

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import log_init, class_attribute_values, class_attribute_names


class DefaultTableModel(QAbstractTableModel):
    def __init__(self, clazz: Type, headers: list = None, cell_alignments: list = None, table_data: list = None,
                 parent: QTableView = None):
        QAbstractTableModel.__init__(self, parent)
        self.clazz = clazz
        self.table_data = table_data or []
        self.headers = headers or self.headers_by_entity()
        self.cell_alignments = cell_alignments or []
        self.log = log_init(AppConfigs.logger())
        self.log.info('{} table_headers={}'.format(clazz.__class__.__name__, '|'.join(self.headers)))

    def data(self, index: QModelIndex, role: int = ...):
        entity = class_attribute_values(self.table_data[index.row()].__dict__)[index.column()]
        str_entity = str(entity) if entity else ''
        if role == Qt.DisplayRole:
            return str_entity
        elif role == Qt.TextAlignmentRole:
            return self.cell_alignments[index.column()] if self.cell_alignments else Qt.AlignLeft
        elif role == Qt.BackgroundColorRole:
            return QVariant() if entity else QColor(230, 230, 230)

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section].upper() if len(self.headers) >= section else '-'
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section
        return QVariant()

    def headers_by_entity(self):
        return class_attribute_names(self.clazz)

    def rowCount(self, parent: QModelIndex = ...):
        return len(self.table_data) if self.table_data and len(self.table_data) > 0 else 0

    def columnCount(self, parent: QModelIndex = ...):
        return len(self.table_data[0].__dict__.keys()) if self.table_data and len(self.table_data) > 0 else 0

    def row(self, index: QModelIndex):
        return self.table_data[index.row()]

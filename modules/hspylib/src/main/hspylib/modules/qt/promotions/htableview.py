#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.qt.promotions
      @file: htableview.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Optional

import pyperclip as clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPainter, QPaintEvent
from PyQt5.QtWidgets import QAbstractScrollArea, QHeaderView, QMenu, QTableView, QWidget


class HTableView(QTableView):
    """TODO"""

    def __init__(self, parent: Optional[QWidget], placeholder: Optional[str] = None):
        super().__init__(parent)
        self._context_menu_enable = True
        self._clearable = True
        self._deletable = True
        self._placeholder = placeholder or 'No data to display'
        self.customContextMenuRequested.connect(self._context_menu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def clear(self):
        """Clear the entire table"""
        model = self.model()
        if model:
            model.clear()

    def paintEvent(self, event: QPaintEvent) -> None:
        """TODO"""
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() > 0:
            return
        color = self.palette().placeholderText().color()
        painter = QPainter(self.viewport())
        painter.save()
        painter.setPen(color)
        elided_text = self.fontMetrics() \
            .elidedText(self._placeholder, Qt.ElideRight, self.viewport().width())
        painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
        painter.restore()

    def copy(self) -> None:
        """Copy selected cell into clipboard"""

        sel_model = self.selectionModel()
        if sel_model:
            index_list = sel_model.selectedIndexes()
            text = ''
            last_row = 0
            for index in index_list:
                if len(text) > 0:
                    if last_row == index.row():
                        text += ' '
                    else:
                        text += '\n'
                text += str(self.model().column(index))
                last_row = index.row()
            clipboard.copy(text)

    def delete(self) -> None:
        """Delete selected rows"""

        self.model().remove_rows(self.model().selected_rows()[0])

    def _context_menu(self):
        """Display the custom context menu"""
        if self._context_menu_enable:
            ctx_menu = QMenu(self)
            ctx_menu.addAction('Copy', self.copy)
            if self._deletable:
                ctx_menu.addAction('Delete', self.delete)
            if self._clearable:
                ctx_menu.addSeparator()
                ctx_menu.addAction('Clear', self.clear)
            ctx_menu.exec_(QCursor.pos())

    def set_context_menu_enable(self, enabled: bool = True):
        """Whether context menu is enabled or not"""
        self._context_menu_enable = enabled

    def set_clearable(self, clearable: bool = True):
        """Whether the widget is clearable or not"""
        self._clearable = clearable

    def set_deletable(self, deletable: bool = True):
        """Whether the widget is clearable or not"""
        self._deletable = deletable

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: htableview.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Optional

import pyperclip as pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QCursor
from PyQt5.QtWidgets import QTableView, QWidget, QMenu, QHeaderView, QAbstractScrollArea


class HTableView(QTableView):
    """TODO"""

    def __init__(self, parent: Optional[QWidget], placeholder: Optional[str] = None):
        super().__init__(parent)
        self.placeholder = placeholder or 'No data to display'
        self.customContextMenuRequested.connect(self._context_menu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def clear(self):
        """TODO"""
        self.model().clear()

    def paintEvent(self, event: QPaintEvent) -> None:
        """TODO"""
        super().paintEvent(event)
        if self.model() is not None and self.model().rowCount() > 0:
            return
        color = self.palette().placeholderText().color()
        painter = QPainter(self.viewport())
        painter.save()
        painter.setPen(color)
        elided_text = self.fontMetrics()\
            .elidedText(self.placeholder, Qt.ElideRight, self.viewport().width())
        painter.drawText(self.viewport().rect(), Qt.AlignCenter, elided_text)
        painter.restore()

    def copy(self) -> None:
        """TODO"""
        text = ''

        index_list = self.selectionModel().selectedIndexes()
        last_row = 0
        for index in index_list:
            if len(text) > 0:
                if last_row == index.row():
                    text += ' '
                else:
                    text += '\n'
            text += str(self.model().column(index))
            last_row = index.row()

        pyperclip.copy(text)

    def _context_menu(self):
        """Display the custom context menu"""
        self._menu = QMenu(self)
        self._menu.addAction(u'Copy', self.copy)
        self._menu.addSeparator()
        self._menu.addAction(u'Clear', self.clear)
        self._menu.exec_(QCursor.pos())

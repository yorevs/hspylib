#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt.promotions
      @file: htableview.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
from typing import Callable, Optional

import pyperclip as clipboard
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPainter, QPaintEvent
from PyQt5.QtWidgets import QAbstractScrollArea, QHeaderView, QMenu, QTableView, QWidget

from hspylib.core.tools.collection_filter import CollectionFilter
from hspylib.core.tools.preconditions import check_argument, check_not_none, check_state
from hspylib.core.tools.text_tools import strip_linebreaks


class HTableView(QTableView):
    """TODO"""

    def __init__(self, parent: Optional[QWidget], placeholder: Optional[str] = None):
        super().__init__(parent)
        self._context_menu_enable = True
        self._copyable = True
        self._clearable = True
        self._deletable = True
        self._placeholder = placeholder or 'No data to display'
        self._custom_menu_actions = []
        self.customContextMenuRequested.connect(self.context_menu)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

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

    def filters(self) -> Optional[CollectionFilter]:
        """TODO"""
        return self.model().filters if self.model() else None

    def refresh(self) -> None:
        self.model().refresh_data()

    def clear(self):
        """Clear the entire table"""
        model = self.model()
        if model:
            model.clear()

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
                        text += '\t'
                    else:
                        text += os.linesep
                text += strip_linebreaks(str(self.model().column(index)))
                last_row = index.row()
            clipboard.copy(text)

    def delete(self) -> None:
        """Delete selected rows"""
        self.model().remove_rows(self.model().selected_rows()[0])

    def context_menu(self) -> None:
        """Display the custom context menu"""
        if self.model().has_data() and self._context_menu_enable:
            ctx_menu = QMenu(self)
            if self._copyable:
                ctx_menu.addAction('Copy Cells', self.copy)
            if self._deletable:
                ctx_menu.addAction('Delete Row', self.delete)
            if self._clearable:
                ctx_menu.addSeparator()
                ctx_menu.addAction('Clear table', self.clear)

            for act in self._custom_menu_actions:
                check_not_none(act)
                check_state(len(act) == 3, f'Invalid custom menu action: {act}')
                check_argument(callable(act[1]), f'The action must be callable')
                if act[2]:
                    ctx_menu.addSeparator()
                ctx_menu.addAction(act[0], act[1])

            ctx_menu.exec_(QCursor.pos())

    def add_custom_menu_action(self, item_text: str, action: Callable, add_separator: bool) -> None:
        action = (item_text, action, add_separator)
        self._custom_menu_actions.append(action)

    def set_context_menu_enable(self, enabled: bool = True) -> None:
        """Whether context menu is enabled or not"""
        self._context_menu_enable = enabled

    def set_copyable(self, copyable: bool = True) -> None:
        """Whether the widget is copyable or not"""
        self._copyable = copyable

    def set_clearable(self, clearable: bool = True) -> None:
        """Whether the widget is clearable or not"""
        self._clearable = clearable

    def set_deletable(self, deletable: bool = True) -> None:
        """Whether the widget is clearable or not"""
        self._deletable = deletable

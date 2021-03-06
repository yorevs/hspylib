#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: hconsole.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QTextCursor, QCursor
from PyQt5.QtWidgets import QWidget, QTextBrowser


class HConsole(QTextBrowser):
    """TODO"""

    def __init__(self, parent: Optional[QWidget], max_lines: int = 1000):
        super().__init__(parent)
        self.setPlaceholderText('No messages received yet')
        self.setReadOnly(True)
        self.setFont(QFont("Courier New", 14))
        self._max_lines = max_lines
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._context_menu)

    def line_count(self) -> int:
        """Return the number of lines the console contains"""
        return self.document().blockCount()

    def is_empty(self) -> bool:
        """Return true if console has no lines"""
        return self.line_count() == 0

    def push_text(self, text: str, color: QColor = None) -> None:
        """Push text to the console. If the maximum buffer size reached,
           the first lines are erased
        """
        fmt_text = f"<font color={color.name() if color else '#FFFFFF'}>{text}</font>"
        if self.line_count() + 1 > self._max_lines:
            self.pop_text()
        self.append(fmt_text)

    def pop_text(self, count: int = 0) -> str:
        """Pop <count> lines form the top->bottom"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, count)
        cursor.select(QTextCursor.LineUnderCursor)
        selected_text = cursor.selectedText()
        cursor.removeSelectedText()
        cursor.deleteChar()
        self.setTextCursor(cursor)

        return selected_text

    def _context_menu(self) -> None:
        """Display the custom context menu"""
        self._menu = self.createStandardContextMenu()
        self._menu.addSeparator()
        self._menu.addAction(u'Clear', self.clear)
        self._menu.exec_(QCursor.pos())

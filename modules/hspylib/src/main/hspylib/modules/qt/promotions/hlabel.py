#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.hspylib.modules.qt.promotions
      @file: hlabel.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetrics, QMouseEvent, QResizeEvent, QTextDocument
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget


class HLabel(QLabel):
    """TODO"""

    clicked = pyqtSignal()
    elisionChanged = pyqtSignal()

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self._clickable = False
        self._elidable = True
        self._dynamic_tooltip = False
        self._content = self.text()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def elidable(self) -> bool:
        return self._elidable

    def set_elidable(self, elidable: bool) -> None:
        self._elidable = elidable

    def clickable(self) -> bool:
        return self._clickable

    def set_clickable(self, clickable: bool) -> None:
        self._clickable = clickable
        self.setCursor(Qt.PointingHandCursor if clickable else Qt.ArrowCursor)

    def dynamic_tooltip(self) -> bool:
        return self._dynamic_tooltip

    def set_dynamic_tooltip(self, dynamic_tooltip: bool) -> None:
        self._dynamic_tooltip = dynamic_tooltip

    def mousePressEvent(self, ev: QMouseEvent) -> None:  # pylint: disable=unused-argument
        if self._clickable:
            self.clicked.emit()

    def setText(self, text: str):
        self._content = text
        if not self.toolTip() or self._dynamic_tooltip:
            self.setToolTip(text)
        if self._elidable:
            metrics = QFontMetrics(self.font())
            max_length = int(self.width() / metrics.maxWidth())
            doc = QTextDocument()
            doc.setHtml(text)
            plain_text = doc.toPlainText()
            if len(plain_text) > max_length:
                self.elisionChanged.emit()
                elided_last_line = metrics.elidedText(text, Qt.ElideRight, self.width())
                super().setText(elided_last_line)
                return
        super().setText(text)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self._content and self._content != self.text():
            self.setText(self._content)
        super().resizeEvent(event)

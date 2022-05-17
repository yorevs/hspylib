#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.qt.promotions
      @file: hframe.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from typing import List, Optional, Union

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget


class HListWidget(QListWidget):
    """TODO"""

    keyPressed = pyqtSignal(int)

    @staticmethod
    def unset_flag(flags: int, flag: int) -> int:
        """TODO"""
        return flags ^ flag if flags & flag == flag else flags

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.editable = False
        self.selectable = True
        self._items = []

    def keyPressEvent(self, event) -> None:
        """TODO"""
        super().keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def addItem(self, item: QListWidgetItem) -> None:
        """TODO"""
        prev = self.item(self.count() - 1)
        if prev:
            item.setFlags(prev.flags())
        super().addItem(item)
        self._items.append(item)

    def set_item(self, item: str, flags: Union[Qt.ItemFlags, Qt.ItemFlag] = None) -> None:
        """TODO"""
        if not self.findItems(item, Qt.MatchFixedString):
            w_item = QListWidgetItem(item)
            w_item.setFlags(flags or Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
            self.addItem(w_item)

    def del_item(self, index: int) -> None:
        """TODO"""
        if 0 < index < len(self._items):
            item = self.takeItem(index)
            if item:
                self._items.remove(self._items[index])

    def index_of(self, item: str) -> int:
        """TODO"""
        return next((obj for obj in self._items if obj == item), None)

    def as_list(self) -> List[str]:
        """TODO"""
        return list(map(QListWidgetItem.text, self._items))

    def text(self) -> str:
        """TODO"""
        return self.currentItem().text()

    def size(self) -> int:
        """TODO"""
        return self.count()

    def set_editable(self, editable: bool = True) -> None:
        """TODO"""
        for item in self._items:
            flags = int(item.flags())
            if editable:
                item.setFlags(flags | Qt.ItemIsEditable)
            else:
                item.setFlags(self.unset_flag(flags, int(Qt.ItemIsEditable)))
            self.editable = editable

    def set_selectable(self, selectable: bool = True) -> None:
        """TODO"""
        for item in self._items:
            flags = int(item.flags())
            if selectable:
                item.setFlags(flags | Qt.ItemIsSelectable)
            else:
                item.setFlags(self.unset_flag(flags, int(Qt.ItemIsSelectable)))
            self.selectable = selectable

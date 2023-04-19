#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Hqt
   @package: hqt.promotions
      @file: htoolbox.py
   @created: Fri, 29 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from functools import cached_property
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, Qt, QVariantAnimation
from PyQt5.QtWidgets import QToolBox


class HToolBox(QToolBox):
    """Animated QToolBox
    Inspired by: https://stackoverflow.com/questions/70746992/animation-effect-in-a-qtoolbox-in-pyqt5-and-python"""

    class _ToolBoxPage(QObject):
        """Animated QToolBox page
        Inspired by: https://stackoverflow.com/questions/70746992/animation-effect-in-a-qtoolbox-in-pyqt5-and-python"""

        QT_MAX_HEIGHT = 16777215

        destroyed = pyqtSignal()

        def __init__(self, button, scroll_area):
            super().__init__()
            self.button = button
            self.scrollArea = scroll_area
            self.widget = scroll_area.widget()
            self.widget.destroyed.connect(self.destroyed)

        def begin_hide(self, spacing):
            """TODO"""
            self.scrollArea.setMinimumHeight(1)
            self.scrollArea.setMaximumHeight(self.scrollArea.height() - spacing)
            if not self.scrollArea.verticalScrollBar().isVisible():
                self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        def begin_show(self, target_height):
            """TODO"""
            if self.scrollArea.widget().minimumSizeHint().height() <= target_height:
                self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            else:
                self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scrollArea.setMaximumHeight(0)
            self.scrollArea.show()

        def set_height(self, height):
            """TODO"""
            if height and not self.scrollArea.minimumHeight():
                self.scrollArea.setMinimumHeight(1)
            self.scrollArea.setMaximumHeight(height)

        def finalize(self):
            """TODO"""
            self.scrollArea.setMinimumHeight(0)
            self.scrollArea.setMaximumHeight(self.QT_MAX_HEIGHT)
            self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    _oldPage = _newPage = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pages = []
        self._targetSize = None

    @cached_property
    def animation(self):
        """TODO"""
        animation = QVariantAnimation(self)
        animation.setDuration(120)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.valueChanged.connect(self._update_sizes)
        return animation

    @pyqtProperty(int)
    def animationDuration(self):
        return self.animation.duration()

    @animationDuration.setter
    def animationDuration(self, duration):
        self.animation.setDuration(max(50, min(duration, 500)))

    @pyqtSlot(int)
    @pyqtSlot(int, bool)
    def setCurrentIndex(self, index, now=False):
        if self.currentIndex() == index:
            return
        if now:
            if self.animation.state():
                self.animation.stop()
                self._pages[index].finalize()
            super().setCurrentIndex(index)
            return
        if self.animation.state():
            return

        self._oldPage = self._pages[self.currentIndex()]
        self._oldPage.begin_hide(self.layout().spacing())
        self._newPage = self._pages[index]
        self._newPage.begin_show(self._targetSize)
        self.animation.start()

    @pyqtSlot(QtWidgets.QWidget)
    @pyqtSlot(QtWidgets.QWidget, bool)
    def setCurrentWidget(self, widget):
        for i, page in enumerate(self._pages):
            if page.widget == widget:
                self.setCurrentIndex(i)
                return

    def itemInserted(self, index):
        button = self.layout().itemAt(index * 2).widget()
        button.clicked.disconnect()
        button.clicked.connect(self._button_clicked)
        scroll_area = self.layout().itemAt(index * 2 + 1).widget()
        page = HToolBox._ToolBoxPage(button, scroll_area)
        self._pages.insert(index, page)
        page.destroyed.connect(self._widget_destroyed)
        self._compute_target_size()

    def itemRemoved(self, index):
        if self.animation.state() and self._index(self._newPage) == index:
            self.animation.stop()
        page = self._pages.pop(index)
        page.destroyed.disconnect(self._widget_destroyed)
        self._compute_target_size()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._compute_target_size()

    def _index(self, page):
        return self._pages.index(page)

    def _update_sizes(self, ratio):
        """TODO"""
        if self.animation.currentTime() < self.animation.duration():
            new_size = round(self._targetSize * ratio)
            old_size = self._targetSize - new_size
            if new_size < self.layout().spacing():
                old_size -= self.layout().spacing()
            self._oldPage.set_height(max(0, old_size))
            self._newPage.set_height(new_size)
        else:
            super().setCurrentIndex(self._index(self._newPage))
            self._oldPage.finalize()
            self._newPage.finalize()

    def _compute_target_size(self):
        """TODO"""
        if not self.count():
            self._targetSize = 0
            return
        _, top, _, bottom = self.getContentsMargins()
        base_height = self._pages[0].button.sizeHint().height() + self.layout().spacing()
        self._targetSize = self.height() - top - bottom - base_height * self.count()

    def _button_clicked(self):
        """TODO"""
        button = self.sender()
        for i, page in enumerate(self._pages):
            if page.button == button:
                self.setCurrentIndex(i)
                return

    def _widget_destroyed(self):
        """TODO"""
        self._pages.remove(self.sender())

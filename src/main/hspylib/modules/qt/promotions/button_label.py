#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt.promotions
      @file: button_label.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class ButtonLabel(QLabel):
    clicked = pyqtSignal(int)
    
    def __init__(self, parent):
        super().__init__(parent=parent)
    
    def mousePressEvent(self, ev) -> None:  # pylint: disable=unused-argument
        self.clicked.emit()

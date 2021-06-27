#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.qt.promotions
      @file: hlabel.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from typing import Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget


class HLabel(QLabel):
    """TODO"""

    clicked = pyqtSignal(int)

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

    def mousePressEvent(self, ev) -> None:  # pylint: disable=unused-argument
        self.clicked.emit()

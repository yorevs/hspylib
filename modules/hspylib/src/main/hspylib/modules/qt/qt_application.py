#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.qt
      @file: qt_application.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC
from typing import TypeVar

from PyQt5.QtWidgets import QApplication

V = TypeVar('V')


class QtApplication(ABC):

    def __init__(self, main_view: V):
        super().__init__()
        self.app = QApplication([])
        self.main_view = main_view()

    def run(self) -> int:
        """Show the main Qt application Widget"""
        self.main_view.show()
        return self.app.exec_()

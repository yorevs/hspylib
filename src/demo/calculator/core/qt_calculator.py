#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.calculator.core
      @file: qt_calculator.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from PyQt5.QtWidgets import QApplication
from calculator.ui.qt.views.main_view import MainView



class QtCalculator:
    def __init__(self):
        self.app = QApplication([])
        self.ui = MainView()
    
    def show(self):
        self.ui.show()
        self.app.exec_()

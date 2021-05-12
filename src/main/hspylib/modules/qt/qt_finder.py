#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt
      @file: qt_finder.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC
from typing import Optional, Type

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QComboBox, QDateEdit, QDialogButtonBox, QDoubleSpinBox, QLabel, QLineEdit, QSpinBox, \
 \
QStackedWidget, QTableView, QToolBox, QToolButton, QWidget


class QtFinder(ABC):
    @staticmethod
    def find_widget(window: QWidget, widget: Type, name: str) -> Optional[QObject]:
        return window.findChild(widget, name)
    
    def __init__(self, window: QWidget):
        super().__init__()
        self.window = window
    
    def find_stacked_widget(self, name: str) -> Optional[QStackedWidget]:
        return QtFinder.find_widget(self.window, QStackedWidget, name)
    
    def find_tool_box(self, name: str) -> Optional[QToolBox]:
        return QtFinder.find_widget(self.window, QToolBox, name)
    
    def find_label(self, name: str) -> Optional[QLabel]:
        return QtFinder.find_widget(self.window, QLabel, name)
    
    def find_tool_button(self, name: str) -> Optional[QToolButton]:
        return QtFinder.find_widget(self.window, QToolButton, name)
    
    def find_table_view(self, name: str) -> Optional[QTableView]:
        return QtFinder.find_widget(self.window, QTableView, name)
    
    def find_line_edit(self, name: str) -> Optional[QLineEdit]:
        return QtFinder.find_widget(self.window, QLineEdit, name)
    
    def find_date_edit(self, name: str) -> Optional[QDateEdit]:
        return QtFinder.find_widget(self.window, QDateEdit, name)
    
    def find_combo_box(self, name: str) -> Optional[QComboBox]:
        return QtFinder.find_widget(self.window, QComboBox, name)
    
    def find_spin_box(self, name: str) -> Optional[QSpinBox]:
        return QtFinder.find_widget(self.window, QSpinBox, name)
    
    def find_double_spin_box(self, name: str) -> Optional[QDoubleSpinBox]:
        return QtFinder.find_widget(self.window, QDoubleSpinBox, name)
    
    def find_button_box(self, name: str) -> Optional[QDialogButtonBox]:
        return QtFinder.find_widget(self.window, QDialogButtonBox, name)

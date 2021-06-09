#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.qt
      @file: qt_finder.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC
from typing import Optional, TypeVar

from PyQt5.QtWidgets import QWidget

W = TypeVar('W')

class QtFinder(ABC):
    """TODO"""

    def find_widget(self, widget: W, name: str) -> Optional[W]:
        """TODO"""
        return self.window.findChild(widget, name)

    def __init__(self, window: QWidget):
        super().__init__()
        self.window = window

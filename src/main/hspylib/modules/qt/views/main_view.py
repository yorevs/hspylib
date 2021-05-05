#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt.views
      @file: main_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import abstractmethod

from PyQt5 import uic

from hspylib.modules.qt.views.qt_view import QtView


class MainView(QtView):
    
    def __init__(self, ui_file_path: str):
        form, window = uic.loadUiType(ui_file_path)
        super().__init__(window)
        self.form = form
        self.form.setupUi(window)
        self.__setup_ui()
    
    @abstractmethod
    def __setup_ui(self) -> None:
        pass
    
    def show(self) -> None:
        self.window.show()

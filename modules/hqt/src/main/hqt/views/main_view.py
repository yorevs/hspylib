#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Hqt
   @package: hqt.views
      @file: main_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from abc import abstractmethod
from hqt.views.qt_view import QtView
from PyQt5 import uic


class MainView(QtView):
    """TODO"""

    def __init__(self, ui_file_path: str):
        form, window = uic.loadUiType(ui_file_path)
        super().__init__(window)
        self.form = form
        self.form.setupUi(window)
        self._setup_ui()

    @abstractmethod
    def _setup_ui(self) -> None:
        """TODO"""

    def show(self) -> None:
        """TODO"""
        self.window.show()

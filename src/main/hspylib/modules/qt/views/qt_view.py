#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.qt.views
      @file: qt_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import os
from abc import ABC
from typing import Tuple, Type

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from hspylib.core.tools.commons import run_dir, new_dynamic_object


class QtView(ABC):
    """TODO"""

    @staticmethod
    def load_ui_form(
        form_file: str,
        load_dir: str = f"{run_dir()}/resources/forms/") -> Tuple[Type, Type]:
        """TODO"""

        assert os.path.exists(load_dir) and os.path.isdir(load_dir), \
            f"Load dir {load_dir} does not exist or is not a folder"
        filepath = f"{load_dir}/{form_file}"
        assert os.path.exists(filepath) and os.path.isfile(filepath) and filepath.lower().endswith('.ui'), \
            f"Form file {form_file} does not exist or it not a valid UI form file"

        return uic.loadUiType(filepath)

    def __init__(self, ui_file: str, parent: QWidget = None):
        form, window = self.load_ui_form(ui_file)
        # Must come after the initialization above {
        self.window = window()
        self.form = form()
        # }
        self.form.setupUi(self.window)
        self.parent = parent
        self.ui = new_dynamic_object('ViewWidgets')
        self._find_widgets()

    def show(self) -> None:
        """TODO"""
        self.window.show()

    def _find_widgets(self):
        """TODO"""
        for widget in self.window.findChildren(QWidget):
            setattr(self.ui, widget.objectName(), widget)

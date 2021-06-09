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
from abc import ABC, abstractmethod
from typing import Tuple, Any, Type

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from hspylib.core.tools.commons import run_dir
from hspylib.modules.qt.qt_finder import QtFinder


class QtView(ABC):
    """TODO"""

    @staticmethod
    def load_ui_form(
        form_file: str,
        load_dir: str = f"{run_dir()}/resources/forms/") -> Tuple[Any, Any]:

        assert os.path.exists(load_dir) and os.path.isdir(load_dir), \
            f"Load dir {load_dir} does not exist or is not a folder"
        filepath = f"{load_dir}/{form_file}"
        assert os.path.exists(load_dir) and os.path.isfile(filepath) and filepath.endswith('.ui'), \
            f"Form file {form_file} does not exist or it not a valid UI form file"

        return uic.loadUiType(filepath)

    def __init__(self, form: Type, window: Type, parent: QWidget = None):
        self.window = window()
        self.form = form()
        self.form.setupUi(self.window)
        self.parent = parent
        self.qt_finder = QtFinder(self.window)

    @abstractmethod
    def setup_ui(self) -> None:
        """TODO"""

    def show(self):
        """TODO"""
        self.window.show()

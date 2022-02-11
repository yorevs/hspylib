#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt.views
      @file: qt_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
import os
from abc import ABC
from typing import Tuple, Type, Optional

from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from hspylib.core.tools.commons import run_dir
from hspylib.core.tools.preconditions import check_argument, check_state


class QtView(ABC):
    """TODO"""

    @staticmethod
    def load_form(
        form_file: str,
        load_dir: str = f"{run_dir()}/resources/forms/") -> Tuple[Type, Type]:
        """Load the ui form from the .ui file"""

        check_argument(os.path.exists(load_dir) and os.path.isdir(load_dir),
                       "Load dir {} does not exist or is not a folder", load_dir)
        filepath = f"{load_dir}/{form_file}"
        check_state(os.path.exists(filepath) and os.path.isfile(filepath) and filepath.lower().endswith('.ui'),
                    "Form file {} does not exist or it not a valid UI form file", form_file)

        return uic.loadUiType(filepath)

    def __init__(self, ui_file: str = 'main_qt_view.ui', parent: Optional[QWidget] = None):
        ui_clazz, window_clazz = self.load_form(ui_file)
        # Must come after the initialization above
        self.window, self.ui = window_clazz(), ui_clazz()
        self.ui.setupUi(self.window)
        self.parent = parent

    def show(self) -> None:
        """Show the main widget"""
        self.window.show()

    def set_default_font(self, default_font: QFont = QFont('Courier New', 14)):
        """Set font for all UI components at once"""
        widgets = list(filter(lambda o: hasattr(getattr(self.ui, o), 'setFont'), vars(self.ui)))
        list(map(lambda w: getattr(self.ui, w).setFont(default_font), widgets))

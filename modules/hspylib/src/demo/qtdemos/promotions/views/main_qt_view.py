#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: main_qt_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.config.app_config import AppConfigs
from hspylib.modules.qt.views.qt_view import QtView


class MainQtView(QtView):
    """TODO"""

    UI_FILE = 'qt_promotions.ui'

    def __init__(self):
        super().__init__(self.UI_FILE)
        self.configs = AppConfigs.INSTANCE
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Connect signals and startup components"""
        pass

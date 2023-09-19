#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.qt.promotions
      @file: hcombobox.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from PyQt5.QtWidgets import QComboBox


class HComboBox(QComboBox):

    def set_item(self, item: str) -> None:
        """TODO"""
        if self.findText(item) < 0:
            self.addItem(item)

    def del_item(self, index: int = -1) -> None:
        """TODO"""
        if index < 0 or index >= self.count():
            if self.currentIndex() >= 0:
                super().removeItem(self.currentIndex())
        else:
            super().removeItem(index)

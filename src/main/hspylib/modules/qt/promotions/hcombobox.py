#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: hcombobox.py
   @created: Wed, 30 Jun 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Optional

from PyQt5.QtWidgets import QComboBox, QWidget


class HComboBox(QComboBox):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)

    def set_item(self, item: str) -> None:
        """TODO"""
        if self.findText(item) < 0:
            self.addItem(item)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Kafman
   @package: kafman.views.promotions
      @file: form_area.py
   @created: Wed, 8 Jun 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from collections import defaultdict
from hqt.promotions.hstacked_widget import HStackedWidget
from kafman.core.schema.widget_utils import InputValue
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractScrollArea, QFrame, QScrollArea, QWidget
from typing import Union

import json


class FormArea(QScrollArea):
    """TODO"""

    keyPressed = pyqtSignal(int)

    @staticmethod
    def _is_not_empty(value: Union[InputValue, dict]) -> bool:
        if isinstance(value, (list, dict)):
            return True
        return str(value) != ""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._form = None
        self.setWidgetResizable(True)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setFrameStyle(QFrame.NoFrame | QFrame.Plain)

    def setWidget(self, widget: QWidget) -> None:
        if self._form is not None:
            assert isinstance(widget, HStackedWidget), "Only HStackedWidget type instances are accepted"
        super().setWidget(widget)
        self._form = widget

    def get_form(self) -> HStackedWidget:
        """TODO"""
        return self._form

    def values(self) -> str:
        """TODO"""

        root = defaultdict()
        current = None
        for pane in self._form.widgets():
            # Filter out empty values
            fields = {k: v for k, v in pane.fields().items() if self._is_not_empty(v)}
            if current is None:
                current = root
                root.update(fields)
            else:
                current = pane[pane.parent_name()].fields()[pane.name()]
                current.update(fields)

        return json.dumps(root, indent=2)

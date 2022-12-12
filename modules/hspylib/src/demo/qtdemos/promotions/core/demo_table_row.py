#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.demo.qtdemos.promotions.core
      @file: demo_table_row.py
   @created: Fri, 29 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional

from PyQt5.QtWidgets import QWidget

from hspylib.modules.qt.promotions.htableview import HTableView


class DemoTableRow(HTableView):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)


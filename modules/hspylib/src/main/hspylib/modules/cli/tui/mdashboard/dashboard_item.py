#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.tui.mdashboard
      @file: dashboard_item.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Callable, Optional

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class DashboardItem:
    """TODO"""

    def __init__(self, icon: Awesome = None, tooltip: str = None, on_trigger: Optional[Callable] = None):
        self.icon = icon
        self.tooltip = tooltip
        self.on_trigger = on_trigger

    def __str__(self):
        return f'{self.icon} "{self.tooltip}" -> {self.on_trigger}'

    def __repr__(self):
        return str(self)

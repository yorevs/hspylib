#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra.mdashboard
      @file: dashboard_item.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from collections import Callable

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class DashboardItem:
    def __init__(
            self,
            icon: Awesome = None,
            tooltip: str = None,
            action: Callable = None):
        self.icon = icon
        self.tooltip = tooltip
        self.action = action

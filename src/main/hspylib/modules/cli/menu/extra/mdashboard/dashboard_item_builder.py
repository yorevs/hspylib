#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra.mdashboard
      @file: dashboard_item_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any, Callable

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.menu.extra.mdashboard.dashboard_item import DashboardItem


class DashboardItemBuilder:
    def __init__(self, parent: Any):
        self.parent = parent
        self.item = DashboardItem()

    def icon(self, icon: Awesome) -> Any:
        self.item.icon = icon
        return self

    def tooltip(self, tooltip: str) -> Any:
        self.item.tooltip = tooltip
        return self

    def action(self, action: Callable) -> Any:
        self.item.action = action
        return self

    def build(self) -> Any:
        self.parent.items.append(self.item)
        return self.parent

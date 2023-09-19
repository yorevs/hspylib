#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.mdashboard
      @file: dashboard_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import List, Optional, Callable

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.tui.mdashboard.dashboard_item import DashboardItem


class DashboardBuilder:
    """Dashboard builder"""

    @staticmethod
    class DashboardItemBuilder:
        """Dashboard item builder"""

        def __init__(self, parent: "DashboardBuilder"):
            self._parent = parent
            self._item = DashboardItem()

        def icon(self, icon: Awesome) -> "DashboardBuilder.DashboardItemBuilder":
            self._item.icon = icon
            return self

        def tooltip(self, tooltip: str) -> "DashboardBuilder.DashboardItemBuilder":
            self._item.tooltip = tooltip
            return self

        def on_trigger(self, on_trigger: Callable) -> Optional["DashboardBuilder.DashboardItemBuilder"]:
            self._item.on_trigger = on_trigger
            return self

        def build(self) -> "DashboardBuilder":
            self._parent.items.append(self._item)
            return self._parent

    def __init__(self):
        self.items = []

    def item(self) -> DashboardItemBuilder:
        return DashboardBuilder.DashboardItemBuilder(self)

    def build(self) -> List[DashboardItem]:
        return self.items

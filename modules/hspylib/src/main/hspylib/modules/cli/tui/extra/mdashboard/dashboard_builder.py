#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui.extra.mdashboard
      @file: dashboard_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Callable, List, Optional

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from hspylib.modules.cli.tui.extra.mdashboard.dashboard_item import DashboardItem


class DashboardBuilder:
    """TODO"""

    @staticmethod
    class DashboardItemBuilder:
        """TODO"""

        def __init__(self, parent: 'DashboardBuilder'):
            self.parent = parent
            self.item = DashboardItem()

        def icon(self, icon: Awesome) -> 'DashboardBuilder.DashboardItemBuilder':
            """TODO"""
            self.item.icon = icon
            return self

        def tooltip(self, tooltip: str) -> 'DashboardBuilder.DashboardItemBuilder':
            """TODO"""
            self.item.tooltip = tooltip
            return self

        def on_trigger(self, on_trigger: Callable) -> Optional['DashboardBuilder.DashboardItemBuilder']:
            """TODO"""
            self.item.on_trigger = on_trigger
            return self

        def build(self) -> 'DashboardBuilder':
            """TODO"""
            self.parent.items.append(self.item)
            return self.parent

    def __init__(self):
        self.items = []

    def item(self) -> DashboardItemBuilder:
        """TODO"""
        return DashboardBuilder.DashboardItemBuilder(self)

    def build(self) -> List[DashboardItem]:
        """TODO"""
        return self.items

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui.mdashboard
      @file: menu_dashboard_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from clitt.core.icons.font_awesome.dashboard_icons import DashboardIcons
from clitt.core.tui.mdashboard.mdashboard import mdashboard, MenuDashBoard

if __name__ == "__main__":
    # fmt: off
    dashboard_items = MenuDashBoard.builder() \
        .item() \
            .icon(DashboardIcons.POWER) \
            .tooltip('Do something') \
            .on_trigger(lambda: print('Something')) \
            .build() \
        .item() \
            .icon(DashboardIcons.MOVIE) \
            .tooltip('Another something') \
            .on_trigger(lambda: print('Another')) \
            .build() \
        .item() \
            .icon(DashboardIcons.NOTIFICATION) \
            .tooltip('Notify something') \
            .on_trigger(lambda: print('Notification')) \
            .build() \
        .item() \
            .icon(DashboardIcons.LIST) \
            .tooltip('List everything') \
            .on_trigger(lambda: print('List')) \
            .build() \
        .item() \
            .icon(DashboardIcons.DATABASE) \
            .tooltip('Database console') \
            .on_trigger(lambda: print('Database')) \
            .build() \
        .item() \
            .icon(DashboardIcons.EXIT) \
            .tooltip('Exit application') \
            .on_trigger(lambda: print('Exit')) \
            .build() \
        .build()
    # fmt: on

    result = mdashboard(dashboard_items)

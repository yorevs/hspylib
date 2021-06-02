#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.cli.tui.extra
      @file: menu_dashboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.menu.extra.mdashboard.mdashboard import MenuDashBoard, mdashboard

from hspylib.modules.cli.icons.font_awesome.dashboard_icons import DashboardIcons

if __name__ == '__main__':
    # @formatter:off
    dashboard_items = MenuDashBoard.builder() \
        .item() \
            .icon(DashboardIcons.PLUS) \
            .tooltip('Add something') \
            .on_trigger(lambda: print('Add')) \
            .build() \
        .item() \
            .icon(DashboardIcons.MINUS) \
            .tooltip('Remove something') \
            .on_trigger(lambda: print('Del')) \
            .build() \
        .item() \
            .icon(DashboardIcons.EDIT) \
            .tooltip('Edit something') \
            .on_trigger(lambda: print('Edit')) \
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
    # @formatter:on
    result = mdashboard(dashboard_items, 4)
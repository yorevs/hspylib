#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.menu.extra.mdashboard
      @file: dashboard_builder.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from typing import Any

from hspylib.modules.cli.menu.extra.mdashboard.dashboard_item_builder import DashboardItemBuilder


class DashboardBuilder:
    def __init__(self):
        self.items = []

    def item(self) -> Any:
        return DashboardItemBuilder(self)

    def build(self) -> list:
        return self.items

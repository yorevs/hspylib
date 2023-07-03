#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.mdashboard
      @file: mdashboard.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.mdashboard.dashboard_item import DashboardItem
from clitt.core.tui.mdashboard.menu_dashboard import MenuDashBoard
from typing import List, Optional


def mdashboard(items: List[DashboardItem], title: str = "Please select one item") -> Optional[DashboardItem]:
    """
    Wrapper for the Menu Dashboard.
    :param items: the provided dashboard items to select from.
    :param title: the title to be displayed before the options.
    """
    return MenuDashBoard(title, items).execute()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: demo.cli.icons.font_awesome
      @file: demo_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from clitt.core.icons.font_awesome.app_icons import AppIcons
from clitt.core.icons.font_awesome.awesome import demo_icons
from clitt.core.icons.font_awesome.dashboard_icons import DashboardIcons
from clitt.core.icons.font_awesome.form_icons import FormIcons
from clitt.core.icons.font_awesome.nav_icons import NavIcons
from clitt.core.icons.font_awesome.widget_icons import WidgetIcons

if __name__ == '__main__':
    print('\nAppIcons ' + '-' * 30)
    demo_icons(awesome=AppIcons, split_columns=10)

    print('\n\nDashboardIcons ' + '-' * 30)
    demo_icons(awesome=DashboardIcons, split_columns=10)

    print('\n\nFormIcons ' + '-' * 30)
    demo_icons(awesome=FormIcons, split_columns=10)

    print('\n\nNavIcons ' + '-' * 30)
    demo_icons(awesome=NavIcons, split_columns=10)

    print('\n\nWidgetIcons ' + '-' * 30)
    demo_icons(awesome=WidgetIcons, split_columns=10)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.icons.font_awesome
      @file: widget_icons.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class WidgetIcons(Awesome):
    """
        Dashboard UI icons.
        Codes can be found here:
        - https://fontawesome.com/cheatsheet?from=io
    """

    # @formatter:off
    WIDGET = '\uFC65'    # ﱥ
    DATABASE = '\uFB19'  # ﬙
    CLOCK = '\uF651'     # 
    NETWORK = '\uF819'   # 
    CHART_1 = '\uFC67'   # ﱨ
    CHART_2 = '\uFC68'   # ﱩ
    MUSIC = '\uFC6E'     # ﱯ
    SIGN = '\uFC7E'      # ﱿ
    SWORDS = '\uFC84'    # ﲅ
    # @formatter:on


if __name__ == '__main__':
    WidgetIcons.demo_icons()

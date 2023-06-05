#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.icons.font_awesome
      @file: widget_icons.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.awesome import Awesome
from enum import auto


class WidgetIcons(Awesome):
    """
    Dashboard UI icons.
    Codes can be found here:
    - https://fontawesome.com/cheatsheet?from=io
    """

    # fmt: off
    _CUSTOM         = auto()
    CHART_2         = '\uF200'  # 
    CHART_1         = '\uF1FE'  # 
    CLOCK           = '\uF651'  # 
    CHIP            = '\uFB19'  # ﬙
    MUSIC           = '\uF3B5'  # 
    NETWORK         = '\uF819'  # 
    PUNCH           = '\uF255'  # 
    SIGN            = '\uF45D'  # 
    WIDGET          = '\uF198'  # 
    # fmt: on

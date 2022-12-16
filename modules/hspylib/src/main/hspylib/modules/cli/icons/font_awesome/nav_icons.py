#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.icons.font_awesome
      @file: app_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from enum import auto

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


# @composable
class NavIcons(Awesome):
    """
    Navigation icons.
    Codes can be found here:
    - https://fontawesome.com/cheatsheet?from=io
    """

    # fmt: off
    _CUSTOM = auto()
    LEFT        = '\u2190'  # ←
    UP          = '\u2191'  # ↑
    RIGHT       = '\u2192'  # →
    DOWN        = '\u2193'  # ↓
    ENTER       = '\u21B2'  # ↲
    TAB         = '\u21B9'  # ↹
    POINTER     = '\uF432'  # 
    SELECTED    = '\uF814'  # 
    UNSELECTED  = '\uF815'  # 
    BREADCRUMB  = '\uF44A'  # 
    # fmt: on

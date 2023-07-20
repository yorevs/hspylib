#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.icons.font_awesome
      @file: nav_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.awesome import Awesome
from enum import auto


# @composable
class NavIcons(Awesome):
    """
    Navigation icons.
    Codes can be found here:
    - https://fontawesome.com/cheatsheet?from=io
    """

    # fmt: off
    _CUSTOM         = auto()
    UP              = '\u2191'  # ↑
    RIGHT           = '\u2192'  # →
    DOWN            = '\u2193'  # ↓
    LEFT            = '\u2190'  # ←
    UP_DOWN         = '\uF9E1'  # 李
    LEFT_RIGHT      = '\uF9E0'  # 易
    ENTER           = '\u21B5'  # ↵
    TAB             = '\u21B9'  # ↹
    BACKSPACE       = '\u232B'  # ⌫
    POINTER         = '\uF432'  # 
    SELECTED        = '\uF814'  # 
    UNSELECTED      = '\uF815'  # 
    BREADCRUMB      = '\uF44A'  # 
    # fmt: on

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.icons.font_awesome
      @file: control_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from enum import auto

from clitt.core.icons.font_awesome.awesome import Awesome


# @composable
class ControlIcons(Awesome):
    """
    Navigation icons.
    Codes can be found here:
    - https://fontawesome.com/cheatsheet?from=io
    """

    # fmt: off
    _CUSTOM         = auto()
    PREVIOUS        = '\uF048'  # 
    REWIND          = '\uF049'  # 
    BACKWARD        = '\uF04A'  # 
    PLAY            = '\uF04B'  # 
    PAUSE           = '\uF04C'  # 
    STOP            = '\uF04D'  # 
    NEXT            = '\uF051'  # 
    ADVANCE         = '\uF050'  # 
    FORWARD         = '\uF04E'  # 
    EJECT           = '\uF052'  # 
    # fmt: on

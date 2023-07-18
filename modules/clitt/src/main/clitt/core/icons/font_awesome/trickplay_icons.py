#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.icons.font_awesome
      @file: trickplay_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.awesome import Awesome
from enum import auto


# @composable
class TrickplayIcons(Awesome):
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

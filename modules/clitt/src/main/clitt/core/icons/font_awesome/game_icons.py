#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.icons.font_awesome
      @file: game_icons.py
   @created: Thu, 20 Jul 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.icons.font_awesome.awesome import Awesome
from enum import auto


# @composable
class GameIcons(Awesome):
    """
    Game icons.
    Codes can be found here:
    - https://fontawesome.com/cheatsheet?from=io
    """

    # fmt: off
    _CUSTOM             = auto()
    STEAM               = '\uF9D2'  # 戮
    XBOX                = '\uFAB8'  # 視
    CUTLERY             = '\uF9A5'  # 殮
    BALL                = '\uF9B7'  # 醴
    HOME                = '\uFAF7'  # 﫷
    FURNITURE           = '\uF9B8'  # 隸
    AGENT               = '\uFAF8'  # 﫸
    GAMEPAD             = '\uFAB9'  # 調
    SWORD               = '\uF9E4'  # 理
    GUN                 = '\uFC01'  # ﰁ
    CANDLE              = '\uFAE1'  # 﫡
    HORSE               = '\uFCC0'  # ﳀ
    MUSHROOM            = '\uFCDD'  # ﳝ
    SHOVEL              = '\uFC0E'  # ﰎ
    BATTLE              = '\uFCFD'  # ﳽ
    WALK                = '\uFC0C'  # ﰌ
    WRITE               = '\uFBD1'  # ﯑
    LOOK                = '\uFBCE'  # ﯎
    EXAMINE             = '\uF422'  # 
    CHAT                = '\uF41F'  # 
    SNOW                = '\uFC15'  # ﰕ
    HOT                 = '\uF490'  # 
    DAY                 = '\uFAA7'  # 盛
    NIGHT               = '\uFA93'  # 望
    TREE                = '\uF904'  # 滑
    KEY                 = '\uF80A'  # 
    OLD_KEY             = '\uF084'  # 
    SLEEP               = '\uF9B1'  # 鈴
    LUCK                = '\uFD14'  # ﴔ
    ANIMAL              = '\uF8E8'  # 
    # fmt: on

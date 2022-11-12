#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.icons.font_awesome
      @file: dashboard_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class DashboardIcons(Awesome):
    """
        Dashboard UI icons.
        Codes can be found here:
        - https://fontawesome.com/cheatsheet?from=io
    """

    # @formatter:off
    ADJUSTMENTS = '\uFB2D'      # שּׂ
    AGENDA = '\uF073'           # 
    ALERT = '\uF071'            # 
    ARCHIVE = '\uF01C'          # 
    BALLOON = '\uF075'          # 
    CAMERA = '\uF030'           # 
    CHAT = '\uF78B'             # 
    CLOUD_DOWNLOAD = '\uF0ED'   # 
    CLOUD_UPLOAD = '\uF0EE'     # 
    CODE = '\uFABF'             # 謹
    COMPASS = '\uF124'          # 
    DASHBOARD = '\uF00A'        # 
    DATABASE = '\uF1C0'         # 
    DELIVERED = '\uFB3D'        # ﬽
    DOCUMENT = '\uF016'         # 
    DOWNLOAD = '\uF019'         # 
    EMAIL = '\uF003'            # 
    ERROR = '\uF06A'            # 
    EXIT = '\uF08B'             # 
    EXPORT = '\uF5F6'           # 
    FAVORITE = '\uF02E'         # 
    FLAG = '\uF024'             # 
    FOLDER = '\uF74A'           # 
    FOLDER_OPEN = '\uF07C'      # 
    FORM = '\uF767'             # 
    FORMAT = '\uF9C5'           # 暈
    HISTORY = '\uF017'          # 
    HOME = '\uF015'             # 
    IDENTITY = '\uF2BB'         # 
    IMPORT = '\uF5F9'           # 
    KILL = '\uFB8A'             # ﮊ
    LIGHT_ON = '\uF834'         # 
    LIGHT_OFF = '\uF835'        # 
    LIKE = '\uF004'             # 
    LIST = '\uF03A'             # 
    LOCATION = '\uF450'         # 
    MOBILE = '\uF61F'           # 
    MOVIE = '\uF008'            # 
    MUSIC = '\uF3B5'            # 
    MUTE = '\uF86C'             # 
    NOTIFICATION = '\uF0F3'     # 
    PICTURE = '\uF03E'          # 
    PLAY = '\uF01D'             # 
    PLUGIN = '\uF930'           # 擄
    PLUG_IN = '\uF1E6'          # 
    PLUG_OUT = '\uF492'         # 
    PLUGGED = '\uFBA3'          # ﮣ
    POWER = '\uF011'            # 
    PRINTER = '\uF02F'          # 
    READ = '\uFB3C'             # לּ
    SAVE = '\uF0C7'             # 
    SEARCH = '\uF002'           # 
    SECRET = '\uF49C'           # 
    SEND = '\uF989'             # 黎
    SENT = '\uF1D8'             # 
    SETTINGS = '\uF013'         # 
    SHOPPING_CART = '\uF60F'    # 
    UN_MUTE = '\uF86B'          # 
    UNPLUGGED = '\uFBA4'        # ﮤ
    USER = '\uF007'             # 
    VERIFIED = '\uFC8F'         # ﲏ

    # @formatter:on


if __name__ == '__main__':
    DashboardIcons.demo_icons()

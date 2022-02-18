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

   Copyright 2021, HSPyLib team
"""
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class DashboardIcons(Awesome):
    """
        Dashboard UI icons.
        Codes can be found here:
        - https://fontawesome.com/cheatsheet?from=io
    """

    # @formatter:off
    SEARCH = '\uF002'        # 
    EMAIL = '\uF003'         # 
    LIKE = '\uF004'          # 
    USER = '\uF007'          # 
    MOVIE = '\uF008'         # 
    DASHBOARD = '\uF00A'     # 
    POWER = '\uF011'         # 
    SETTINGS = '\uF013'      # 
    ADJUSTMENTS = '\uFB2D'   # שּׂ
    HOME = '\uF015'          # 
    DOCUMENT = '\uF016'      # 
    HISTORY = '\uF017'       # 
    DELIVERED = '\uFB3D'     # ﬽
    READ = '\uFB3C'          # לּ
    DOWNLOAD = '\uF019'      # 
    ARCHIVE = '\uF01C'       # 
    PLAY = '\uF01D'          # 
    FLAG = '\uF024'          # 
    FAVORITE = '\uF02E'      # 
    PRINTER = '\uF02F'       # 
    CAMERA = '\uF030'        # 
    LIST = '\uF03A'          # 
    CODE = '\uFABF'          # 謹
    FORM = '\uF767'          # 
    FORMAT = '\uF9C5'        # 暈
    PICTURE = '\uF03E'       # 
    ERROR = '\uF06A'         # 
    ALERT = '\uF071'         # 
    AGENDA = '\uF073'        # 
    CHAT = '\uF075'          # 
    SHOPPING = '\uF07A'      # 
    GRAPHS = '\uF080'        # 
    FOLDER = '\uF74A'        # 
    FOLDER_OPEN = '\uF07C'   # 
    EXIT = '\uF08B'          # 
    SEND = '\uF989'          # 黎
    SENT = '\uF1D8'          # 
    COMPASS = '\uF124'       # 
    TWITTER = '\uF081'       # 
    FACEBOOK = '\uF082'      # 
    LINKED_IN = '\uF08C'     # 
    GRAPH = '\uF08F'         # 
    SAVE = '\uF0C7'          # 
    CLOUD_DOWN = '\uF0ED'    # 
    CLOUD_UP = '\uF0EE'      # 
    NOTIFICATION = '\uF0F3'  # 
    DATABASE = '\uF1C0'      # 
    PLUGIN = '\uF930'        # 擄
    PLUG_IN = '\uF1E6'       # 
    PLUG_OUT = '\uF492'      # 
    UNPLUGGED = '\uFBA4'     # ﮤ
    PLUGGED = '\uFBA3'       # ﮣ
    KILL = '\uFB8A'          # ﮊ
    IDENTITY = '\uF2BB'      # 
    DOCKER = '\uF308'        # 
    MUSIC = '\uF3B5'         # 
    MUTE = '\uF86B'          # 
    UNMUTE = '\uF86C'        # 
    SECRET = '\uF49C'        # 
    IE = '\uF7FF'            # 
    GIT = '\uF813'           # 
    VERIFIED = '\uFC8F'      # ﲏ
    LIGHT_ON = '\uF834'      # 
    LIGHT_OFF = '\uF835'     # 
    PYTHON = '\uF81F'        # 
    JAVA = '\uF4E4'          # 
    CPLUSPLUS = '\uFB70'     # ﭱ
    GITHUB = '\uF408'        # 
    CLOUD_PUT = '\uF40A'     # 
    CLOUD_GET = '\uF409'     # 
    EXPORT = '\uF5F6'        # 
    IMPORT = '\uF5F9'        # 
    # @formatter:on


if __name__ == '__main__':
    DashboardIcons.demo_icons()

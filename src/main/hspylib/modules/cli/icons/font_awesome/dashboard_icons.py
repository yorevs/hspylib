#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.main.hspylib.modules.cli.icons.font_awesome
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
    SEARCH = u'\uF002'       # 
    EMAIL = u'\uF003'        # 
    LIKE = u'\uF004'         # 
    USER = u'\uF007'         # 
    MOVIE = u'\uF008'        # 
    DASHBOARD = u'\uF00A'    # 
    POWER = u'\uF011'        # 
    SETTINGS = u'\uF013'     # 
    HOME = u'\uF015'         # 
    DOCUMENT = u'\uF016'     # 
    HISTORY = u'\uF017'      # 
    DOWNLOAD = u'\uF019'     # 
    ARCHIVE = u'\uF01C'      # 
    PLAY = u'\uF01D'         # 
    REFRESH = u'\uF01E'      # 
    FLAG = u'\uF024'         # 
    FAVORITE = u'\uF02E'     # 
    PRINTER = u'\uF02F'      # 
    CAMERA = u'\uF030'       # 
    LIST = u'\uF03A'         # 
    PICTURE = u'\uF03E'      # 
    ERROR = u'\uF06A'        # 
    ALERT = u'\uF071'        # 
    AGENDA = u'\uF073'       # 
    CHAT = u'\uF075'         # 
    SHOPPING = u'\uF07A'     # 
    GRAPHS = u'\uF080'       # 
    FOLDER = u'\uF74A'       # 
    FOLDER_OPEN = u'\uF07C'  # 
    EXIT = u'\uF08B'         # 
    SEND = u'\uF989'         # 黎
    SENT = u'\uF1D8'         # 
    COMPASS = u'\uF124'      # 
    TWITTER = u'\uF081'      # 
    FACEBOOK = u'\uF082'     # 
    LINKED_IN = u'\uF08C'    # 
    GRAPH = u'\uF08F'        # 
    SAVE = u'\uF0C7'         # 
    CLOUD_DOWN = u'\uF0ED'   # 
    CLOUD_UP = u'\uF0EE'     # 
    NOTIFICATION = u'\uF0F3' # 
    DATABASE = u'\uF1C0'     # 
    CONNECT = u'\uF1E6'      # 
    DISCONNECT = u'\uF492'   # 
    IDENTITY = u'\uF2BB'     # 
    DOCKER = u'\uF308'       # 
    MUSIC = u'\uF3B5'        # 
    SECRET = u'\uF49C'       # 
    IE = u'\uF7FF'           # 
    GIT = u'\uF813'          # 
    VERIFIED = u'\uFC8F'     # ﲏ
    LIGHT_ON = u'\uF834'     # 
    LIGHT_OFF = u'\uF835'    # 
    PYTHON = u'\uF81F'       # 
    JAVA = u'\uF4E4'         # 
    GITHUB = u'\uF408'       # 
    CLOUD_PUT = u'\uF40A'    # 
    CLOUD_GET = u'\uF409'    # 

    # @formatter:on

if __name__ == '__main__':
    DashboardIcons.demo_icons()

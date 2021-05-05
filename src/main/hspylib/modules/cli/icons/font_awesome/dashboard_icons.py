#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.icons.font_awesome
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
    
    SEARCH = '\uF002'  # 
    EMAIL = '\uF003'  # 
    LIKE = '\uF004'  # 
    USER = '\uF007'  # 
    MOVIE = '\uF008'  # 
    DASHBOARD = '\uF00A'  # 
    POWER = '\uF011'  # 
    SETTINGS = '\uF013'  # 
    HOME = '\uF015'  # 
    DOCUMENT = '\uF016'  # 
    HISTORY = '\uF017'  # 
    DOWNLOAD = '\uF019'  # 
    ARCHIVE = '\uF01C'  # 
    PLAY = '\uF01D'  # 
    REFRESH = '\uF01E'  # 
    FLAG = '\uF024'  # 
    FAVORITE = '\uF02E'  # 
    PRINTER = '\uF02F'  # 
    CAMERA = '\uF030'  # 
    LIST = '\uF03A'  # 
    PICTURE = '\uF03E'  # 
    EDIT = '\uF040'  # 
    PLUS = '\uF067'  # 
    MINUS = '\uF068'  # 
    ERROR = '\uF06A'  # 
    ALERT = '\uF071'  # 
    AGENDA = '\uF073'  # 
    CHAT = '\uF075'  # 
    SHOPPING = '\uF07A'  # 
    GRAPHS = '\uF080'  # 
    FOLDER = '\uF74A'  # 
    FOLDER_OPEN = '\uF07C'  # 
    EXIT = '\uF08B'  # 
    TWITTER = '\uF081'  # 
    FACEBOOK = '\uF082'  # 
    LINKED_IN = '\uF08C'  # 
    GRAPH = '\uF08F'  # 
    SAVE = '\uF0C7'  # 
    CLOUD_DOWN = '\uF0ED'  # 
    CLOUD_UP = '\uF0EE'  # 
    NOTIFICATION = '\uF0F3'  # 
    DATABASE = '\uF1C0'  # 
    CONNECT = '\uF1E6'  # 
    IDENTITY = '\uF2BB'  # 
    DOCKER = '\uF308'  # 
    MUSIC = '\uF3B5'  # 
    SECRET = '\uF49C'  # 


if __name__ == '__main__':
    DashboardIcons.demo_icons()

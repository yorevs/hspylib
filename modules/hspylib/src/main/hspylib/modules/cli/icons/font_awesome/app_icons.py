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
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome

class AppIcons(Awesome):
    """
        Application icons.
        Codes can be found here:
        - https://fontawesome.com/cheatsheet?from=io
    """

    # @formatter:off
    APPLE = '\uF534'            # 
    AWS = '\uF375'              # 
    CPLUSPLUS = '\uFB70'        # ﭱ
    DOCKER = '\uF308'           # 
    DROPBOX = '\uF6E2'          # 
    GIT = '\uF813'              # 
    GITHUB = '\uF408'           # 
    GOOGLE_DRIVE = '\uF3AA'     # 
    FACEBOOK = '\uF082'         # 
    FIREBASE = '\uF1D0'         # 
    IE = '\uF7FF'               # 
    JAVA = '\uF4E4'             # 
    LINKED_IN = '\uF08C'        # 
    PYTHON = '\uF81F'           # 
    STACK_OVERFLOW = '\uF9CB'   # 溜
    TWITTER = '\uF081'          # 
    VS_CODE = '\uFB0F'          # ﬏
    WHATSAPP = '\uFAA2'         # 甆
    # @formatter:on


if __name__ == '__main__':
    AppIcons.demo_icons()

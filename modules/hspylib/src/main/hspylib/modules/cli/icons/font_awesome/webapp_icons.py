#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.icons.font_awesome
      @file: webapp_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class WebappIcons(Awesome):
    """
        Dashboard UI icons.
        Codes can be found here:
        - https://fontawesome.com/cheatsheet?from=io
    """

    # @formatter:off
    GITHUB = '\uF408'           # 
    TWITTER = '\uF081'          # 
    FACEBOOK = '\uF082'         # 
    LINKED_IN = '\uF08C'        # 
    STACK_OVERFLOW = '\uF9CB'   # 溜
    DROPBOX = '\uFC29'          # ﰩ
    # @formatter:on


if __name__ == '__main__':
    WebappIcons.demo_icons()

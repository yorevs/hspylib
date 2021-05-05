#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.modules.cli.icons.font_awesome
      @file: form_icons.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class FormIcons(Awesome):
    """
        Form UI icons.
        Codes can be found here:
        - https://fontawesome.com/cheatsheet?from=io
    """
    
    ARROW_LEFT = '\uF060'  # 
    ARROW_RIGHT = '\uF061'  # 
    ARROW_UP = '\uF062'  # 
    ARROW_DOWN = '\uF063'  # 
    
    CHECK = '\uF00C'  # 
    ERROR = '\uf057'  # 
    CHECK_CIRCLE = '\uF058'  # 
    UNCHECK_CIRCLE = '\uF111'  # 
    CHECK_SQUARE = '\uF14A'  # 
    UNCHECK_SQUARE = '\uF0C8'  # 
    ON = '\uF205'  # 
    OFF = '\uF204'  # 
    
    HIDDEN = '\uF070'  # 
    VISIBLE = '\uF06E'  # 
    LOCKED = '\uF023'  # 
    UNLOCKED = '\uF09C'  # 
    EDITABLE = '\uF044'  # 
    DELETE = '\uF014'  # 


if __name__ == '__main__':
    FormIcons.demo_icons()

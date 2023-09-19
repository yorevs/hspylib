#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.main.hspylib.addons.appman
      @file: appman_enums.py
   @created: Fri, 29 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration

class Extension(Enumeration):
    """Appman available extensions"""
    GRADLE = 'gradle'
    GIT = 'git'


class AppType(Enumeration):
    """Appman supported application types"""
    APP = 'app'
    QT_APP = 'qt-app'
    WIDGET = 'widget'

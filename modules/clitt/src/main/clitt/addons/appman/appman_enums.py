#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.addons.appman
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

    # fmt: off
    GRADLE  = 'gradle'
    GIT     = 'git'
    # fmt: on


class AppType(Enumeration):
    """Appman supported application types"""

    # fmt: off
    APP     = 'app'
    QT_APP  = 'qt-app'
    WIDGET  = 'widget'
    # fmt: on

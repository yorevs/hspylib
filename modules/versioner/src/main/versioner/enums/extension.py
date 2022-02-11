#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.versioner.enums
      @file: extension.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from hspylib.core.enums.enumeration import Enumeration


class Extension(Enumeration):
    DEVELOPMENT = 1
    SNAPSHOT = 2
    STABLE = 4
    RELEASE = 8

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

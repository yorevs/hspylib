#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.versioner.src.main.enums
      @file: part.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class Part(Enumeration):
    PATCH = 1
    MINOR = 2
    MAJOR = 4

    def __str__(self):
        return str(self.name).lower()

    def __repr__(self):
        return str(self)

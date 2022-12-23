#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: clitt.core.tui.minput
      @file: access_type.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class AccessType(Enumeration):
    """TODO"""

    NO_ACCESS = "no-access"
    READ_ONLY = "read-only"
    READ_WRITE = "read-write"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.minput
      @file: access_type.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from hspylib.core.enums.enumeration import Enumeration


class AccessType(Enumeration):
    """MenuInput input field access types."""

    # fmt: off
    NO_ACCESS   = "no-access"
    READ_ONLY   = "read-only"
    READ_WRITE  = "read-write"
    # fmt: on

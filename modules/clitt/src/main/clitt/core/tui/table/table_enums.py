#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.core.tui.table
      @file: table_enums.py
   @created: Tue, 4 Jul 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from enum import auto
from hspylib.core.enums.enumeration import Enumeration
from hspylib.core.tools.text_tools import *
from typing import Callable


class TextAlignment(Enumeration):
    """Table cell/header text justification helper."""

    # fmt: off
    LEFT    = auto(), justified_left
    CENTER  = auto(), justified_center
    RIGHT   = auto(), justified_right
    # fmt: on

    def val(self) -> Callable:
        return self.value[1]


class TextCase(Enumeration):
    """Table cell/header text case helper."""

    # fmt: off
    TITLE   = auto(), titlecase
    SNAKE   = auto(), snakecase
    CAMEL   = auto(), camelcase
    KEBAB   = auto(), kebabcase
    LOWER   = auto(), lowercase
    UPPER   = auto(), uppercase
    # fmt: on

    def val(self) -> Callable:
        return self.value[1]

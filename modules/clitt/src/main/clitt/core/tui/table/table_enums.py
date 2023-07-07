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
from hspylib.core.tools import text_tools
from typing import Callable


class TextAlignment(Enumeration):
    """Table cell/header text justification helper."""

    # fmt: off
    LEFT    = auto(), text_tools.justified_left
    CENTER  = auto(), text_tools.justified_center
    RIGHT   = auto(), text_tools.justified_right
    # fmt: on

    def val(self) -> Callable:
        return self.value[1]


class TextCase(Enumeration):
    """Table cell/header text case helper."""

    # fmt: off
    TITLE   = auto(), text_tools.titlecase
    SNAKE   = auto(), text_tools.snakecase
    CAMEL   = auto(), text_tools.camelcase
    KEBAB   = auto(), text_tools.kebabcase
    LOWER   = auto(), text_tools.lowercase
    UPPER   = auto(), text_tools.uppercase
    # fmt: on

    def val(self) -> Callable:
        return self.value[1]

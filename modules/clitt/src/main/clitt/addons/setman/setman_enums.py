#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: setman_enums.py
   @created: Fri, 29 May 2023
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from typing import List

from hspylib.core.enums.enumeration import Enumeration


class SetmanOps(Enumeration):
    """Setman operations."""

    # fmt: off
    GET         = 'get'
    SET         = 'set'
    DEL         = 'del'
    LIST        = 'list'
    SEARCH      = 'search'
    TRUNCATE    = 'truncate'
    # fmt: on

    @staticmethod
    def choices() -> List[str]:
        return SetmanOps.values()


class SettingsType(Enumeration):
    """Settings types."""

    # fmt: off
    ENVIRONMENT = 'environment'
    PROPERTY    = 'property'
    # fmt: on

    @staticmethod
    def choices() -> List[str]:
        return SettingsType.values()

    @staticmethod
    def selectables(selected: str = '') -> str:
        return '|'.join([s if selected != s else f"<{s}>" for s in SettingsType.values()])

    @property
    def val(self) -> str:
        return str(self.value)

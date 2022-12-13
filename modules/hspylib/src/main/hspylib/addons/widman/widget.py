#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.hspylib.addons.widman
      @file: widget.py
   @created: Fri, 29 Jul 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from abc import ABC, abstractmethod
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome
from textwrap import dedent
from typing import List


class Widget(ABC):
    """HSPyLib_Widman base class. All widgets must inherit from this class to properly work."""

    _USAGE_FMT = dedent(
        """
    HSPyLib Widget: {} v{}

    {}

    {}
    """
    )

    def __init__(self, icon: Awesome, name: str, tooltip: str, usage: str, version: Version):
        self._icon = icon
        self._name = name
        self._tooltip = tooltip
        self._usage = usage
        self._version = version

    @abstractmethod
    def execute(self, args: List[str] = None) -> ExitStatus:
        """Execute the widget main flow"""

    def cleanup(self) -> None:
        """Execute the widget cleanup"""

    def icon(self) -> Awesome:
        return self._icon

    def name(self) -> str:
        """Return the name about the widget"""
        return self._name

    def tooltip(self) -> str:
        """Return information about the widget"""
        return self._tooltip

    def version(self) -> str:
        """Return the version of the widget"""
        return str(self._version)

    def usage(self) -> str:
        """Return a usage message about the widget"""
        return self._USAGE_FMT.format(self._name, self._version, self._tooltip, self._usage)

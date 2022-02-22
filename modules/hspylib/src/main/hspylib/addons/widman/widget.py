#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   main.addons.widman
      @file: widget.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from hspylib.core.enums.exit_code import ExitCode
from hspylib.modules.cli.icons.font_awesome.awesome import Awesome


class Widget(ABC):
    """HSPyLib Widgets base class. All widgets must inherit from this class"""

    _USAGE_FMT = """
HSPyLib Widget: {} v{}

{}

{}
"""

    def __init__(
        self,
        icon: Awesome,
        name: str,
        tooltip: str,
        usage: str,
        version: Tuple[int, int, int]):
        self._icon = icon
        self._name = name
        self._tooltip = tooltip
        self._usage = usage
        self._version = version

    @abstractmethod
    def execute(self, args: List[str] = None) -> ExitCode:
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

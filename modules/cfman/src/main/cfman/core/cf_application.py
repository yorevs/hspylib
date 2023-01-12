#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-CFMan
   @package: cfman.core
      @file: cf_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.exception.exceptions import InvalidArgumentError
from hspylib.core.tools.commons import sysout
from typing import List

import re


class CFApplication:
    """Represent a PCF application.
    """

    max_name_length = 70

    @classmethod
    def of(cls, app_line: str):
        """Create a cf application entry from the cf apps output line.
        """
        parts = re.split(r" {2,}", app_line)
        # format: name | state | instances | memory | disk | urls
        if len(parts) == 6:  # Old cf command output
            return CFApplication(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5].split(", "))
        # format: name | state | type:i/o | urls
        if len(parts) == 4:  # New cf command output
            if not (mat := re.search(r"(\w+):(\d+/\d+)", parts[2])):
                raise InvalidArgumentError(f"Invalid application line: \"{app_line}\"")
            instances = mat.group(2)
            memory = disk = "-"
            return CFApplication(parts[0], parts[1], instances, memory, disk, parts[3].split(", "))

        raise InvalidArgumentError(f"Invalid application line: {app_line}")

    def __init__(self, name: str, state: str, instances: str, memory: str, disk: str, urls: List[str]) -> None:
        self.prefs: TUIPreferences = TUIPreferences.INSTANCE or TUIPreferences()
        self.name = name
        self.state = state
        self.instances = instances
        self.memory = memory
        self.disk = disk
        self.urls = urls
        self.max_name_length = max(self.max_name_length, len(self.name))

    def __str__(self) -> str:
        return f"[{self.colored_state}] {self.name}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def colored_state(self) -> str:
        """Return the actual application state using colors.
        """
        state = self.state.upper()
        return f"{self.prefs.success_color if self.is_started else self.prefs.error_color:5}{state}" \
            + self.prefs.text_color.code

    @property
    def is_started(self) -> bool:
        return self.state.lower() == 'started'

    # pylint: disable=consider-using-f-string
    def print_status(self) -> None:
        """Print the actual application status line.
        """
        sysout(
            "%CYAN%{}  {:5}  %NC%{:10}  {:4}  {:4}  {}".format(
                self.name.ljust(self.max_name_length),
                self.colored_state,
                self.instances,
                self.memory,
                self.disk,
                self.urls,
            )
        )

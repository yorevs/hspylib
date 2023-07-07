#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-CFMan
   @package: cfman.core
      @file: cf_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.terminal import Terminal
from clitt.core.tui.tui_preferences import TUIPreferences
from hspylib.core.exception.exceptions import InvalidArgumentError
from typing import List

import re


class CFApplication:
    """Represent a PCF application."""

    max_name_length = 70

    @classmethod
    def of(cls, app_line: str):
        """Create a cf application entry from the cf apps output line."""
        parts = re.split(r" {2,}", app_line)
        # format: name | state | instances | memory | disk | urls
        if len(parts) == 6:  # Old CF command output
            return CFApplication(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5].split(", "))
        # format: name | requested state | processes | routes
        if len(parts) == 4:  # New CF command output
            if not (mat := re.search(r"(\w+):(\d+/\d+)", parts[2])):
                raise InvalidArgumentError(f'Invalid application line: "{app_line}"')
            instances = mat.group(2)
            memory = disk = "-"
            return CFApplication(parts[0], parts[1], instances, memory, disk, parts[3].split(","))

        raise InvalidArgumentError(
            f"Invalid application line: " f"{app_line}" f"Probably CF APPS command changed the command output."
        )

    def __init__(self, name: str, state: str, instances: str, memory: str, disk: str, routes: List[str]) -> None:
        self.prefs: TUIPreferences = TUIPreferences.INSTANCE
        self.name = name
        self.state = state
        self.instances = instances
        self.memory = memory
        self.disk = disk
        self.routes = routes
        self.max_name_length = max(self.max_name_length, len(self.name))

    def __str__(self) -> str:
        return f"[{self.colored_state}] {self.name}"

    def __repr__(self) -> str:
        return str(self)

    @property
    def colored_state(self) -> str:
        """Return the actual application state using colors."""
        state = self.state.upper()
        return (
            f"{self.prefs.success_color if self.is_started else self.prefs.error_color}"
            f"{state:<7}{self.prefs.text_color.code}"
        )

    @property
    def is_started(self) -> bool:
        return self.state.lower() == "started"

    def print_status(self) -> None:
        """Print the actual application status line."""
        Terminal.echo(
            f"%CYAN%{self.name:<{self.max_name_length + 2}}"
            f"{self.colored_state:}  %NC%{self.instances:<12}{self.memory:<6}{self.disk:<6}{len(self.routes)}"
        )

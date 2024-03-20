#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.core.tui
      @file: tui_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import os
import sys

from hspylib.core.metaclass.classpath import AnyPath
from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version

from clitt.core.term.screen import screen
from clitt.core.term.terminal import terminal


class TUIApplication(Application, metaclass=AbstractSingleton):
    """Terminal UI application base class."""

    def __init__(
        self,
        name: str | None,
        version: Version = Version.initial(),
        description: str = None,
        usage: str = None,
        epilog: str = None,
        resource_dir: AnyPath = None,
        log_dir: AnyPath = None,
    ):
        super().__init__(name, version, description, usage, epilog, resource_dir, log_dir)
        self._app_name = os.path.basename(sys.argv[0]) if name is None else name

    def _setup_arguments(self) -> None:
        pass

    def _main(self, *params, **kwargs) -> ExitStatus:
        pass

    def _cleanup(self) -> None:
        if screen.alternate and self._exit_code == ExitStatus.SUCCESS:
            screen.alternate = not screen.alternate
        terminal.restore()

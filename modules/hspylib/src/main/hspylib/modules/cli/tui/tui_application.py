#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.cli.tui
      @file: tui_application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.metaclass.singleton import AbstractSingleton
from hspylib.modules.application.application import Application
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.vt100.vt_utils import alternate_screen


class TUIApplication(Application, metaclass=AbstractSingleton):
    """TODO"""

    def __init__(
        self,
        name: str,
        version: Version,
        description: str = None,
        usage: str = None,
        epilog: str = None,
        resource_dir: str = None,
        log_dir: str = None
    ):
        super().__init__(name, version, description, usage, epilog, resource_dir, log_dir)
        self._alt_screen = False

    def _setup_arguments(self) -> None:
        pass

    def _main(self, *params, **kwargs) -> ExitStatus:
        pass

    def _cleanup(self) -> None:
        if self._alt_screen and self._exit_code == ExitStatus.SUCCESS:
            self._alternate_screen()

    def _alternate_screen(self):
        self._alt_screen = not self._alt_screen
        alternate_screen(self._alt_screen)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import sys


class ExitHooks:
    """TODO"""

    def __init__(self):
        self._orig_exit = None
        self.exit_code = None
        self.exception = None

    def hook(self) -> None:
        """TODO"""
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0) -> None:
        """TODO"""
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc, *args) -> None:  # pylint: disable=unused-argument
        """TODO"""
        self.exception = exc

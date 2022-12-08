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
import traceback
from typing import Callable

from hspylib.core.tools.commons import syserr

EXIT_CB = Callable[[], None]

class ExitHooks:
    """TODO"""

    def __init__(self, cleanup: EXIT_CB = None):
        self._orig_exit = None
        self._exit_code = None
        self._exception = None
        self._traceback = None
        self._cleanup = cleanup

    def hook(self) -> None:
        """TODO"""
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exception_hook

    def exit(self, code=0) -> None:
        """TODO"""
        self._exit_code = code
        self._orig_exit(code)

    def exception_hook(
        self, exc_type: TypeError | None, exc: BaseException | None,
        tb: traceback) -> None:
        """TODO"""

        self._exception, self._traceback = exc, tb
        tb = "\t".join(traceback.format_exception(exc_type, exc, self._traceback))
        syserr(tb)
        if self._cleanup:
            self._cleanup()

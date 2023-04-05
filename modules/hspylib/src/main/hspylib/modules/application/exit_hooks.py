#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.modules.application
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
from hspylib.modules.application.exit_status import ExitStatus

CLEANUP_CB = Callable[[], None]
EXIT_CB = Callable[[int | ExitStatus], None]


class ExitHooks:
    """TODO"""

    def __init__(self, cleanup: CLEANUP_CB = None):
        self._orig_exit: EXIT_CB = sys.exit
        self._exit_status: ExitStatus = ExitStatus.SUCCESS
        self._exception = None
        self._traceback = None
        self._was_hooked: bool = False
        self._cleanup: CLEANUP_CB = cleanup
        sys.exit = self.exit

    def hook(self) -> None:
        """TODO"""
        sys.excepthook = self.exception_hook

    def exit(self, code: ExitStatus | int | None) -> None:
        """TODO"""
        self._exit_status = ExitStatus.of(code or 0)
        if not self._was_hooked:
            self._orig_exit(self._exit_status.val)
        else:
            exit(self._exit_status.val)

    def exception_hook(self, exc_type: TypeError | None, exc: BaseException | None, tb: traceback) -> None:
        """TODO"""

        self._was_hooked = True
        self._exception, self._traceback = exc, tb
        tb = "\t".join(traceback.format_exception(exc_type, exc, self._traceback))
        syserr(tb)
        if self._cleanup:
            self._cleanup()

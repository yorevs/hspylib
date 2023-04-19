#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.modules.application
      @file: application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from hspylib.core.tools.commons import syserr
from hspylib.modules.application.exit_status import ExitStatus
from typing import Callable, Optional

import sys
import traceback

CLEANUP_CB = Optional[Callable[[], None]]

EXIT_CB = Callable[[int | ExitStatus], None]

EXIT_STATUS = Optional[ExitStatus | int]


class ExitHooks:
    """Provide application exit hooks."""

    def __init__(self, cleanup: CLEANUP_CB = None):
        self._orig_exit: EXIT_CB = sys.exit
        self._exit_status: ExitStatus = ExitStatus.SUCCESS
        self._exception = None
        self._traceback = None
        self._was_hooked: bool = False
        self._cleanup: CLEANUP_CB = cleanup
        sys.exit = self.exit

    def hook(self) -> None:
        """Set the default system exception hook to this hook."""
        sys.excepthook = self.except_hook

    def exit(self, exit_status: EXIT_STATUS) -> None:
        """Exit the application with the specified exit status."""
        self._exit_status = ExitStatus.of(int(exit_status or 0))
        if not self._was_hooked:
            self._orig_exit(int(self._exit_status))
        else:
            exit(int(self._exit_status))

    def except_hook(self, exc_type: TypeError | None, exc: BaseException | None, tb: traceback) -> None:
        """Handle a system exception."""
        self._was_hooked = True
        self._exception, self._traceback = exc, tb
        tb = "\t".join(traceback.format_exception(exc_type, exc, self._traceback))
        syserr(tb)
        if self._cleanup:
            self._cleanup()

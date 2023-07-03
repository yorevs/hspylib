#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.decorator
      @file: decorators.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datetime import datetime, timedelta
from hspylib.core.tools.commons import str_to_bool
from math import ceil
from typing import Any, Callable

import logging as log
import os
import signal
import unittest


def integration_test(cls: type):
    """Enable/Disable HsPyLib integration tests"""

    it_disabled = str_to_bool(os.environ.get("HSPYLIB_IT_DISABLED", "True"))
    if it_disabled:
        log.debug("Skipping test: %s", cls.__name__)
        return unittest.skipIf(
            it_disabled, f"Disabled = {it_disabled} :integration tests because it needs real servers running"
        )

    return cls


def temporized(func: Callable):
    """Log the time spent on the Callable invocation."""

    def timedelta_to_str(delta: timedelta) -> str:
        """Convert timedelta object into string"""
        parts = str(delta).split(":")
        h, m, s = parts[0], parts[1], parts[2][:-7]
        ms = int(ceil(int(parts[2][-6:]) / 1000))
        return f"{h:02s}[h] {m:02s}[m] {s:02s}[s] {ms:02d}[ms]"

    def temporized_closure(*args) -> Any:
        """Execute the callable and return"""
        start = datetime.now()
        ret = func(*args)
        log.debug("@@@ [%s] Time elapsed\t%s", func.__name__, timedelta_to_str(datetime.now() - start))
        return ret

    return temporized_closure


def hooksignals(signals: tuple | signal.Signals):
    def helper(func: Callable[[int, Any], None]):
        # Here, we will see the functionality of the code:
        sig_numbers: tuple = signals if isinstance(signals, tuple) else (signals,)
        list(map(lambda s: signal.signal(s, func), sig_numbers))

    return helper

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.shared
      @file: decorators.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
import unittest
from datetime import datetime, timedelta
from math import ceil
from typing import Callable

from hspylib.core.tools.commons import str_to_bool


def integration_test(cls: type):
    """Enable/Disable HsPyLib integration tests"""

    it_disabled = str_to_bool(os.environ.get('HSPYLIB_IT_DISABLED', 'True'))
    if it_disabled:
        log.debug('Skipping test: ', cls.__name__)
        return unittest.skipIf(
            it_disabled,
            f'Disabled = {it_disabled} :integration tests because it needs real servers running'
        )

    return cls


def temporized(func: Callable):
    """Log the time spent on the Callable invocation."""

    def timedelta_to_str(delta: timedelta) -> str:
        """TODO"""
        parts = str(delta).split(':')
        h, m, s = parts[0], parts[1], parts[2][:-7]
        ms = int(ceil(int(parts[2][-6:]) / 1000))
        return f"{h:02s}[h] {m:02s}[m] {s:02s}[s] {ms:02d}[ms]"

    def wrapper(*args):
        start = datetime.now()
        ret = func(*args)
        log.debug(f"@@@ [{func.__name__}] Time elapsed\t{timedelta_to_str(datetime.now() - start)}")
        return ret

    return wrapper

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: hspylib.core.decorator
      @file: decorators.py
   @created: Tue, 11 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
import inspect
import logging as log
import os
import signal
import unittest
from datetime import datetime, timedelta
from functools import partial
from typing import Any, Callable

from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import to_bool


def integration_test(cls: type):
    """Enable/Disable HsPyLib integration tests"""

    it_disabled = to_bool(os.environ.get("HSPYLIB_IT_DISABLED", "True"))
    if it_disabled:
        log.debug("Skipping test: %s", cls.__name__)
        return unittest.skipIf(
            it_disabled, f"Disabled = {it_disabled} :integration tests because it needs real servers running"
        )

    return cls


def profiled(func: Callable):
    """Log the time spent on the Callable invocation."""

    def timedelta_to_str(delta: timedelta) -> str:
        """Convert timedelta object into string."""
        parts = str(delta).split(":")
        h, m, s = parts[0], parts[1], parts[2][:-7]
        ms = int(int(parts[2][-6:]) / 1000)
        return f"{h:02s}[h] {m:02s}[m] {s:02s}[s] {ms:02d}[ms]"

    def profiled_closure(*args, **kwargs) -> Any:
        """Execute the callable and return."""
        start = datetime.now()
        ret = func(*args, **kwargs)
        elapsed = datetime.now() - start
        print(f"@@@ [{func.__name__:>20}] Time elapsed\t{timedelta_to_str(elapsed)}")
        return ret

    return profiled_closure


def hook_signals(signals: tuple[signal.Signals, ...] | signal.Signals):
    """
    Decorator to hook a function to specific signals. When the specified signal(s) occur, the decorated function
    will be invoked.

    :param signals: A tuple of signal numbers or a single signal. These signals will be hooked to the function.
    """

    def helper(func: Callable):
        """Helper function that takes the function to be decorated, hooks it to the specified signal(s), and returns
        the wrapped function."""
        handler_signature = inspect.signature(func)
        args: list = []
        for param in handler_signature.parameters.values():
            if param.default == inspect.Parameter.empty and param.kind not in \
                [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD]:
                args.append(param)
        count = len(args)

        check_argument(
            count >= 2, f"Signal handlers require the following arguments: (signum and frame). Given: '{count}'")

        sig_numbers = signals if isinstance(signals, tuple) else (signals,)

        def wrapped_function():
            """'helper' wrapper that supports instance methods as well as functions."""

            # If the first argument is 'self', bind the signal handler accordingly
            if count > 2 and inspect.isclass(type(args[0])):
                self = args[0]  # The first argument is 'self'
                for s in sig_numbers:
                    signal.signal(s, partial(func, self))
            else:
                for s in sig_numbers:
                    signal.signal(s, func)

        # Immediately set up the signal handler
        wrapped_function()

        return wrapped_function

    return helper

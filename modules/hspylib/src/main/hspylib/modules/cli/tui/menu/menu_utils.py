#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.tui
      @file: menu_utils.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import time
from abc import ABC
from typing import Any, Callable, Optional

from hspylib.core.exception.exceptions import InputAbortedError
from hspylib.core.tools.commons import syserr, sysout
from hspylib.core.tools.validator import Validator
from hspylib.modules.cli.vt100.vt_colors import VtColors


class MenuUtils(ABC):
    """TODO"""

    @staticmethod
    def print_error(
        message: str,
        argument: Any = None,
        wait_interval: int = 2) -> None:
        """TODO"""

        syserr(f"### Error: {message} \"{argument or ''}\"")
        time.sleep(wait_interval)
        sysout('%CUU(2)%%ED0%', end='')

    @staticmethod
    def print_warning(
        message: str,
        argument: str = None,
        wait_interval: int = 2,
        color: VtColors = VtColors.YELLOW) -> None:
        """TODO"""

        sysout(f"{color.placeholder()}### Warn: {message} \"{argument or ''}\"")
        time.sleep(wait_interval)
        sysout('%CUU(2)%%ED0%', end='')

    @staticmethod
    def prompt(
        prompt_msg: str = '',
        validator: Callable = None,
        default_value: Any = None,
        any_key: bool = False,
        on_blank_abort: bool = True,
        color: VtColors = VtColors.GREEN,
        end: str = ': ') -> Optional[Any]:
        """TODO"""

        valid = False
        input_data = None

        while not valid:
            try:
                colorized = VtColors.colorize(
                    f"{color.placeholder()}{prompt_msg}{f'[{default_value}]' if default_value else ''}{end}{VtColors.NC.placeholder()}"
                )
                input_data = input(colorized)
                if not validator:
                    valid = True
                elif default_value:
                    return default_value
                elif any_key:
                    return None
                elif Validator.is_not_blank(input_data):
                    valid, msg = validator(input_data)
                    if not valid:
                        MenuUtils.print_error(f"{msg}: ", input_data)
                else:
                    if not on_blank_abort:
                        MenuUtils.print_error("Input can't be empty: ", input_data)
                    else:
                        raise InputAbortedError('Input process was aborted')
            except EOFError as err:
                MenuUtils.print_error("Input failed: ", str(err))
                break

        return input_data

    @staticmethod
    def wait_enter(
        wait_msg: str = 'Press [Enter] to continue ...',
        color: VtColors = VtColors.YELLOW) -> None:
        """TODO"""
        MenuUtils.prompt(wait_msg, any_key=True, color=color, end='')

    @staticmethod
    def title(title_str: str, color: VtColors = VtColors.YELLOW) -> None:
        """TODO"""
        sysout(f"%ED2%%HOM%\n{color.placeholder()}{title_str}\n")

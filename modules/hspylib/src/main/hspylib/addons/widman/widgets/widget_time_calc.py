#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file

   @project: HSPyLib
   @package: main.addons.widman.widgets
      @file: widget_time_calc.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import math
import re
from typing import List, Optional, Tuple

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_status import ExitStatus
from hspylib.core.exception.exceptions import WidgetExecutionError
from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.tui.extra.minput.minput import MenuInput, minput


class WidgetTimeCalc(Widget):
    """HSPyLib Widget to calculate time based operations"""

    WIDGET_ICON = WidgetIcons.CLOCK
    WIDGET_NAME = "TimeCalc"
    TOOLTIP = "Calculate time based operations."
    USAGE = "Usage: TimeCalc [+d|++decimal] <HH1:MM1[:SS1]> <+|-> <HH2:MM2[:SS2]>"
    VERSION = (0, 1, 0)

    @staticmethod
    def to_decimal(time_raw: int = 0) -> int:
        """ Convert a raw time into decimal """
        return int(round(((time_raw / 60.00) * 100.00)))

    @staticmethod
    def calc_time(args: List[str]) -> Tuple[int, int, int]:
        """Calculate the time resulted from the specified operations."""
        op, total_seconds = '+', 0
        for tm in args:
            if not tm:
                continue
            if re.match(r"[+-]", tm):
                op = tm
            elif re.match(r"^([0-9]{1,2}:?)+", tm):
                try:
                    parts = [int(math.floor(float(s))) for s in tm.split(':')]
                except ValueError as err:
                    raise WidgetExecutionError(f"Unable to extract time parts from '{tm}'") from err
                f_hours = parts[0] if len(parts) > 0 else 0
                f_minutes = parts[1] if len(parts) > 1 else 0
                f_secs = parts[2] if len(parts) > 2 else 0
                tm_amount = ((f_hours * 60 + f_minutes) * 60 + f_secs)
                if op == '+':
                    total_seconds += tm_amount
                elif op == '-':
                    total_seconds -= tm_amount
            else:
                raise WidgetExecutionError(f"Invalid time input: '{tm}'")
        total_seconds, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(abs(total_seconds), 60)

        return hours if total_seconds > 0 else -1 * hours, minutes, seconds

    def __init__(self) -> None:
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)

        self._decimal = False
        self._args = None

    def _parse_args(self, args: List[str]) -> Optional[ExitStatus]:
        """Parse command line arguments"""

        if not args and not self._read_args():
            return ExitStatus.ABORTED
        if args and any(a in args for a in ['+h', '++help']):
            sysout(self.usage())
            return ExitStatus.SUCCESS
        if args and any(a in args for a in ['+v', '++version']):
            sysout(self.version())
            return ExitStatus.SUCCESS

        if args and any(a in args for a in ['+d', '++decimal']):
            self._decimal = True
            args = args[1:]

        if not self._args:
            self._args = args

        return None

    def execute(self, args: List[str] = None) -> ExitStatus:

        ret_val = self._parse_args(args)

        if ret_val is not None:
            return ret_val

        hours, minutes, seconds = self.calc_time(self._args)

        if self._decimal:
            print(f"{hours:02d}.{self.to_decimal(minutes):02d}.{self.to_decimal(seconds):02d}")
        else:
            print(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        return ExitStatus.SUCCESS

    def _read_args(self) -> bool:
        """ When no input is provided (e.g:. when executed from dashboard). Prompt the user for the info. """
        # @formatter:off
        form_fields = MenuInput.builder() \
            .field() \
                .label('Time 1') \
                .itype('masked') \
                .value('|##:##:##') \
                .build() \
            .field() \
                .label('Operation') \
                .itype('select') \
                .value('+|-') \
                .build() \
            .field() \
                .label('Time 2') \
                .itype('masked') \
                .value('|##:##:##') \
                .build() \
            .build()
        # @formatter:on

        result = minput(form_fields)
        self._args = result.values if result else None
        sysout('%HOM%%ED2%%MOD(0)%', end='')

        return bool(result)

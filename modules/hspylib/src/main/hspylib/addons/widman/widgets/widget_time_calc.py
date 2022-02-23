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

   Copyright 2021, HSPyLib team
"""

import math
import re
from typing import List, Optional

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
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

    def __init__(self):
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)

        self.total_seconds = 0
        self.op = '+'
        self.decimal = False
        self.args = None

    def parse_args(self, args: List[str]) -> Optional[ExitCode]:
        """TODO"""

        if (not args or len(args) < 3) or not any(a in args for a in ['+h', '++help']):
            if not self._read_args():
                return ExitCode.ERROR
        elif args[0] in ['+h', '++help']:
            sysout(self.usage())
            return ExitCode.SUCCESS
        elif args[0] in ['+v', '++version']:
            sysout(self.version())
            return ExitCode.SUCCESS
        elif args[0] in ['+d', '++decimal']:
            self.decimal = True
            args = args[1:]

        if not self.args:
            self.args = args

        return None

    def execute(self, args: List[str] = None) -> ExitCode:
        """TODO"""

        ret_val = self.parse_args(args)

        if ret_val is not None:
            return ret_val

        for tm in self.args:
            if re.match(r"[+-]", tm):
                self.op = tm
            elif re.match(r"^([0-9]{1,2}:?)+", tm):
                try:
                    parts = [int(math.floor(float(s))) for s in tm.split(':')]
                except ValueError:
                    return ExitCode.ERROR
                f_hours = parts[0] if len(parts) > 0 else 0
                f_minutes = parts[1] if len(parts) > 1 else 0
                f_secs = parts[2] if len(parts) > 2 else 0
                tm_amount = ((f_hours * 60 + f_minutes) * 60 + f_secs)

                if self.op == '+':
                    self.total_seconds += tm_amount
                elif self.op == '-':
                    self.total_seconds -= tm_amount
            else:
                raise WidgetExecutionError(f"Invalid time input: '{tm}'")

        self.total_seconds, seconds = divmod(self.total_seconds, 60)
        hours, minutes = divmod(self.total_seconds, 60)

        sysout('%HOM%%ED2%%MOD(0)%', end='')
        if self.decimal:
            sysout(f"{hours:02d}.{self._decimal(minutes):02d}.{self._decimal(seconds):02d}")
        else:
            sysout(f"{hours:02d}:{self._decimal(minutes):02d}:{self._decimal(seconds):02d}")

        return ExitCode.SUCCESS

    def _decimal(self, time_raw: int = 0) -> int:
        """ Convert a raw time into decimal """
        return int(round(((time_raw / 60.00) * 100.00) if self.decimal else time_raw))

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
        self.args = [value for _, value in result.__dict__.items()] if result else []

        return bool(result)

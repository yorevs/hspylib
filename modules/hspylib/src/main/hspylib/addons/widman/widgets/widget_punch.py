#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: hspylib.addons.widman.widgets
      @file: widget_punch.py
   @created: Thu, 20 Sep 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import argparse
import os
import re
import sys
from textwrap import dedent
from typing import List

from hspylib.addons.widman.widget import Widget
from hspylib.addons.widman.widgets.widget_time_calc import WidgetTimeCalc
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import syserr, sysout
from hspylib.core.zoned_datetime import now
from hspylib.modules.application.argparse.argument_parser import HSArgumentParser
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.vt100.terminal import Terminal


class WidgetPunch(Widget):
    """HSPyLib Widget to Report current system memory usage"""

    # fmt: off
    WIDGET_ICON = WidgetIcons.PUNCH
    WIDGET_NAME = "Punch"
    VERSION     = Version(0, 1, 0)
    TOOLTIP     = "!!! PUNCH THE CLOCK !!!"
    USAGE       = dedent("""
    "Usage: ${FUNCNAME[0]} [options] <args>"

      Options: '
        -l        : List all registered punches.'
        -e        : Edit current punch file.'
        -r        : Reset punches for the current week and save the previous one.'
        -w <week> : Report (list) all punches of specified week using the pattern: week-N.punch.'

      Notes: '
        When no arguments are provided it will !!PUNCH THE CLOCK!!.'
    """)
    # fmt: on

    HHS_DIR = os.getenv("HHS_PUNCH_FILE", os.getenv("HOME", "./"))

    HHS_PUNCH_FILE = os.getenv("HHS_PUNCH_FILE", f"-{HHS_DIR}/.punches")

    DATE_STAMP = now("%a %d-%m-%Y")

    TIME_STAMP = now("%H:%M")

    WEEK_STAMP = int(now("%V"))

    RE_TODAY_PUNCH_LINE = rf"({DATE_STAMP}).*"

    RE_PUNCH_LINE = r"^((Mon|Tue|Wed|Thu|Fri|Sat|Sun) )(([0-9]+-?)+) =>.*"

    MAX_PUNCHES = 7  # 7 week days

    @staticmethod
    def _daily_total(daily_punches: List[str], decimal: bool = False) -> str:
        """Calculate the total time from the daily punches."""
        # Up to 3 pairs of timestamps: morning, afternoon and evening
        if (n := len(daily_punches)) > 0 and n % 2 == 0:
            stamps = []
            stamps += [daily_punches[1], "-", daily_punches[0], "+"] if n // 2 >= 1 else []  # Morning
            stamps += [daily_punches[3], "-", daily_punches[2], "+"] if n // 2 >= 2 else []  # Afternoon
            stamps += [daily_punches[5], "-", daily_punches[4]] if n // 2 >= 3 else []  # Evening
            h, m, _ = WidgetTimeCalc.calc_time(stamps)
            m = WidgetTimeCalc.to_decimal(m) if decimal else m
            return f"{'%GREEN%' if h >= 8 else '%RED%'}{h:02d}{'.' if decimal else ':'}{m:02d}%NC%"

        return f"%RED%--{'.' if decimal else ':'}--%NC%"

    def __init__(self) -> None:
        super().__init__(self.WIDGET_ICON, self.WIDGET_NAME, self.TOOLTIP, self.USAGE, self.VERSION)

        self._exit_code = ExitStatus.SUCCESS
        self._fn = self._do_the_punch
        self._args = None
        self._today = None
        self._punches = []
        self._total_hour = self._total_min = 0
        self._week_num = self.WEEK_STAMP

    def execute(self, args: List[str] = None) -> ExitStatus:

        # Create the current week punch file if it does not yet exist.
        if not os.path.exists(self.HHS_PUNCH_FILE):
            with open(self.HHS_PUNCH_FILE, "w", encoding=Charset.UTF_8.val) as f_punch:
                f_punch.write(f"{now('%d-%m-%Y')} => ")

        ret_val = self._parse_args(args)

        if not ret_val:
            return ExitStatus.ABORTED

        if self._args:
            if "list" == self._args.action:
                self._punches = self._read_punches(self.HHS_PUNCH_FILE)
                self._fn = self._list_punches
            elif "week" == self._args.action:
                punch_dir = os.path.dirname(self.HHS_PUNCH_FILE)
                self._week_num = self._args.week_num
                self._punches = self._read_punches(f"{punch_dir}/week-{self._week_num:02d}.punch")
                self._fn = self._list_punches
            elif "edit" == self._args.action:
                self._fn = self._edit_punches
            elif "reset" == self._args.action:
                self._fn = self._reset_punches
        else:
            self._punches = self._read_punches(self.HHS_PUNCH_FILE)

        self._fn()

        return ExitStatus.SUCCESS

    def _parse_args(self, args: List[str]) -> bool:
        """Parse command line arguments"""

        if not args:
            return True

        parser = HSArgumentParser(
            prog="punch",
            prefix_chars="+",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="PUNCH-THE-CLOCK. This is a helper tool to aid with the timesheet.",
        )

        subparsers = parser.add_subparsers(title="action", dest="action")
        subparsers.add_parser("list", help="list all registered punches.")
        subparsers.add_parser("edit", help="edit current punch file.")
        subparsers.add_parser("reset", help="reset punches for the current week and save the previous one.")

        w_parser = subparsers.add_parser("week", help="list all punches of the specified week-num (week-N.punch).")
        w_parser.add_argument("week_num", type=int, default=1, help="the week number")

        self._args = parser.parse_args(args)

        return bool(self._args)

    def _read_punches(self, punch_file: str) -> List[str]:
        """Read all punches from the punch file."""
        if not os.path.exists(punch_file):
            syserr(f"Punch file '{punch_file}' not found !")
            raise FileNotFoundError(f"Punch file '{punch_file}' not found !")

        with open(punch_file, "r", encoding=Charset.UTF_8.val) as f_punch:
            all_punches = list(
                map(self._set_today, filter(lambda l: re.match(self.RE_PUNCH_LINE, l), f_punch.readlines()))
            )
            if len(all_punches) > self.MAX_PUNCHES:
                sysout(f"%RED%Punch file contains more than {self.MAX_PUNCHES} punch lines !%NC%")
                sys.exit(int(str(ExitStatus.FAILED.value)))
            return all_punches

    def _is_today(self, punch_line: str) -> bool:
        """Whether the punch line refer to today's date."""
        return bool(re.match(self.RE_TODAY_PUNCH_LINE, punch_line))

    def _set_today(self, punch_line: str) -> str:
        """Set the today's date if the line represents today."""
        if not self._today and self._is_today(punch_line):
            self._today = punch_line
        return punch_line

    def _do_the_punch(self) -> None:
        """!!DO THE PUNCH!!"""
        with open(self.HHS_PUNCH_FILE, "w", encoding=Charset.UTF_8.val) as f_punch:
            if not self._today:  # Write the first punch of the day
                self._today = f"{self.DATE_STAMP} => {self.TIME_STAMP}"
                self._punches.append(self._today)
            elif self._today.count(":") < 6:  # Only allowed 3 groups of 3 pairs of punches
                pat = rf"({self.DATE_STAMP}) => (.*)"
                if mat := re.match(pat, self._today):
                    self._today = re.sub(pat, f"{mat.group(1)} => {mat.group(2)} {self.TIME_STAMP} ", self._today)
                else:
                    raise Exception("Invalid punch file")
                self._punches[-1] = self._today
            list(map(f_punch.write, [f"{punch.strip()}\n" for punch in self._punches]))
        sysout(f"{re.sub(self.DATE_STAMP, '%GREEN%Today%NC%', self._today)} ")

    def _list_punches(self) -> None:
        """List all punches from the punch file."""
        total = 0, 0
        total_dec = 0, 0
        sysout(f"\n%WHITE%Week-{self._week_num:02d} Punches%NC%")
        sysout("-" * 82)
        for punch_line in self._punches:
            daily_punches = punch_line[17:].strip().split()
            n = len(daily_punches)
            padding = "." * (35 if n == 0 else (36 - n * 6))
            line_color = "%BLUE%" if self._is_today(punch_line) else ""
            sysout(f"{line_color}{punch_line[:17]} {' '.join(daily_punches) + (' ' if n % 2 != 0 else '')}", end="")
            daily_total = self._daily_total(daily_punches)
            daily_total_dec = self._daily_total(daily_punches, decimal=True)
            if n > 0 and n % 2 == 0:
                sysout(f" {padding} : Subtotal = {daily_total} -> {daily_total_dec}%NC%")
                total = WidgetTimeCalc.calc_time([f"{total[0]}:{total[1]}", "+", daily_total[-9:-4]])
                total_dec = total[0], WidgetTimeCalc.to_decimal(total[1])
            else:
                sysout(f"{daily_total}%NC%")
        sysout("-" * 82)
        bh, bm, _ = WidgetTimeCalc.calc_time([f"{total[0]}:{total[1]}", "-", "40:00"])
        balance = f"{'%BLUE%' if bh >= 0 else '%RED%'}{bh:02d}:{bm:02d}%NC%"
        totals = f"{total[0]:02d}:{total[1]:02d} -> {total_dec[0]:02d}.{total_dec[1]:02d}"
        sysout(f"%WHITE%Total: ({totals})  Balance: {balance}\n")

    def _edit_punches(self) -> None:
        """Open the default system editor to edit punches."""
        Terminal.open(self.HHS_PUNCH_FILE)

    def _reset_punches(self) -> None:
        """Rename the punch file as a weekly punch file and reset current punch file."""
        punch_dir = os.path.dirname(self.HHS_PUNCH_FILE)
        new_name = f"{punch_dir}/week-{self._week_num:02d}.punch"
        if os.path.exists(new_name):
            sysout(f"%RED%Punch file '{new_name}' already exists!")
        else:
            os.rename(self.HHS_PUNCH_FILE, new_name)
            sysout(f"%YELLOW%Punch file {self.HHS_PUNCH_FILE} renamed to {new_name}")

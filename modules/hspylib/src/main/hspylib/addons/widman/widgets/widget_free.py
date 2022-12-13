#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file

   @project: HSPyLib
   @package: main.addons.widman.widgets
      @file: widget_free.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from concurrent import futures
from hspylib.addons.widman.widget import Widget
from hspylib.core.tools.commons import human_readable_bytes, sysout
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.keyboard import Keyboard
from hspylib.modules.cli.vt100.terminal import Terminal
from textwrap import dedent
from time import sleep
from typing import List

import re


class WidgetFree(Widget):
    """HSPyLib Widget to Report current system memory usage"""

    # fmt: off
    WIDGET_ICON = WidgetIcons.CHIP
    WIDGET_NAME = "Free"
    VERSION     = Version(0, 2, 0)
    TOOLTIP     = "Report system memory usage."
    USAGE       = "Usage: Free"
    # fmt: on

    def __init__(self) -> None:
        super().__init__(self.WIDGET_ICON, self.WIDGET_NAME, self.TOOLTIP, self.USAGE, self.VERSION)
        self._is_alive = True
        self._report_interval = 1.5
        self._exit_code = ExitStatus.SUCCESS

    def execute(self, args: List[str] = None) -> ExitStatus:
        with futures.ThreadPoolExecutor() as executor:
            done = False
            while not done and not Keyboard.kbhit():
                future = executor.submit(self._report_usage)
                done = not future.result()
                if not done:
                    sleep(self._report_interval)
        return self._exit_code

    # pylint: disable=too-many-locals
    @staticmethod
    def _report_usage() -> bool:
        """Display the memory usage for the cycle"""
        ps, ec1 = Terminal.shell_exec("ps -caxm -orss,comm")  # Get process info
        vm, ec2 = Terminal.shell_exec("vm_stat")  # Grabbing memory characteristics

        if ec1 == ExitStatus.SUCCESS and ec2 == ExitStatus.SUCCESS and ps:
            process_lines = ps.split("\n")  # Iterate processes
            sep = re.compile(" +")
            rss_total = 0  # kB

            for row in range(1, len(process_lines)):
                row_text = process_lines[row].strip()
                row_elements = sep.split(row_text)
                if re.match("^[0-9]+$", row_elements[0]):
                    rss = float(row_elements[0]) * 1024
                else:
                    rss = 0
                rss_total += rss

            vm_lines = vm.split("\n")  # Process vm_stat
            sep = re.compile(": +")
            vm_stats = {}

            for row in range(1, len(vm_lines) - 2):
                row_text = vm_lines[row].strip()
                row_elements = sep.split(row_text)
                vm_stats[(row_elements[0])] = int(row_elements[1].strip("\\.")) * 4096

            wired, wu = human_readable_bytes(vm_stats["Pages wired down"])
            active, au = human_readable_bytes(vm_stats["Pages active"])
            inactive, iu = human_readable_bytes(vm_stats["Pages inactive"])
            free, fu = human_readable_bytes(vm_stats["Pages free"])
            real, ru = human_readable_bytes(rss_total)  # Total memory

            sysout(
                dedent(
                    f"""
            %HOM%%ED2%%MOD(0)%
            %ORANGE%Reporting system memory usage:%NC%
            {'-' * 30}
            %GREEN%   Wired Memory: {wired:6s} {wu:2s}
            %GREEN%  Active Memory: {active:6s} {au:2s}
            %GREEN%Inactive Memory: {inactive:6s} {iu:2s}
            %GREEN%    Free Memory: {free:6s} {fu:2s}
            %GREEN%    Real Memory: {real:6s} {ru:2s}

            %YELLOW%Press [Enter] to exit ..."""
                )
            )

            return True

        return False

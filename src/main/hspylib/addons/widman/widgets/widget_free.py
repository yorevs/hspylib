#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.main.hspylib.addons.widman.widgets
      @file: widget_free.py
   @created: Thu, 20 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import re

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
from hspylib.core.tools.commons import human_readable_bytes, sysout
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons
from hspylib.modules.cli.menu.menu_utils import MenuUtils
from hspylib.modules.cli.vt100.terminal import Terminal


class WidgetFree(Widget):

    WIDGET_ICON  = WidgetIcons.DATABASE
    WIDGET_NAME = "Free"
    TOOLTIP = "Report system memory usage."
    USAGE = "Usage: Free"
    VERSION = (0, 2, 0)

    def __init__(self):
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)


    def execute(self, *args) -> ExitCode:
        # Get process info
        ps = Terminal.shell_exec('ps -caxm -orss,comm')
        vm = Terminal.shell_exec('vm_stat')

        # Iterate processes
        process_lines = ps.split('\n')
        sep = re.compile(' +')
        rss_total = 0  # kB

        for row in range(1, len(process_lines)):
            row_text = process_lines[row].strip()
            row_elements = sep.split(row_text)
            if re.match('^[0-9]+$', row_elements[0]):
                rss = float(row_elements[0]) * 1024
            else:
                rss = 0
            rss_total += rss

        # Process vm_stat
        vm_lines = vm.split('\n')
        sep = re.compile(': +')
        vm_stats = {}

        for row in range(1, len(vm_lines) - 2):
            row_text = vm_lines[row].strip()
            row_elements = sep.split(row_text)
            vm_stats[(row_elements[0])] = int(row_elements[1].strip('\\.')) * 4096

        wired, wu = human_readable_bytes(vm_stats["Pages wired down"])
        active, au = human_readable_bytes(vm_stats["Pages active"])
        inactive, iu = human_readable_bytes(vm_stats["Pages inactive"])
        free, fu = human_readable_bytes(vm_stats["Pages free"])
        real, ru = human_readable_bytes(rss_total)  # Total memory

        sysout('%HOM%%ED2%%MOD(0)%', end='')
        sysout(f"\n%ORANGE%Reporting system memory usage:%NC% \n{'-' * 30}")
        sysout(f"    %GREEN%Wired Memory%NC%: {wired:6s} {wu:2s}")
        sysout(f"   %GREEN%Active Memory%NC%: {active:6s} {au:2s}")
        sysout(f" %GREEN%Inactive Memory%NC%: {inactive:6s} {iu:2s}")
        sysout(f"     %GREEN%Free Memory%NC%: {free:6s} {fu:2s}")
        sysout(f"     %GREEN%Real Memory%NC%: {real:6s} {ru:2s}")
        sysout(' ')

        MenuUtils.wait_enter()

        return ExitCode.SUCCESS

    def cleanup(self):
        pass

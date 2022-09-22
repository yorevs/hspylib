#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file

   @project: HSPyLib
   @package: main.addons.widman.widgets
      @file: widget_punch.py
   @created: Thu, 20 Sep 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
from textwrap import dedent
from typing import List

from hspylib.addons.widman.widget import Widget
from hspylib.core.enums.exit_code import ExitCode
from hspylib.core.tools.commons import sysout
from hspylib.core.tools.zoned_datetime import now
from hspylib.modules.cli.icons.font_awesome.widget_icons import WidgetIcons


class WidgetPunch(Widget):
    """HSPyLib Widget to Report current system memory usage"""

    WIDGET_ICON = WidgetIcons.PUNCH
    WIDGET_NAME = "Punch"
    TOOLTIP = "!!! PUNCH THE CLOCK !!!"
    USAGE = dedent("""
    "Usage: ${FUNCNAME[0]} [options] <args>"

      Options: '
        -l        : List all registered punches.'
        -e        : Edit current punch file.'
        -r        : Reset punches for the current week and save the previous one.'
        -w <week> : Report (list) all punches of specified week using the pattern: week-N.punch.'

      Notes: '
        When no arguments are provided it will !!PUNCH THE CLOCK!!.'
    """)
    VERSION = (0, 1, 0)

    HHS_DIR = os.getenv('HHS_PUNCH_FILE', os.getenv('HOME', './'))

    HHS_PUNCH_FILE = os.getenv('HHS_PUNCH_FILE', f"-{HHS_DIR}/.punches")

    DATE_STAMP='%a %d-%m-%Y'

    TIME_STAMP='%H:%M'

    WEEK_STAMP='%V'

    def __init__(self):
        super().__init__(
            self.WIDGET_ICON,
            self.WIDGET_NAME,
            self.TOOLTIP,
            self.USAGE,
            self.VERSION)

        self._exit_code = ExitCode.SUCCESS

    def execute(self, args: List[str] = None) -> ExitCode:

        if args and args[0] in ['-h', '--help']:
            sysout(self.usage())
            return ExitCode.SUCCESS
        if args and args[0] in ['-v', '--version']:
            sysout(self.version())
            return ExitCode.SUCCESS

        date_stamp = now('%d-%m-%Y')

        # Create the punch file if it does not exist
        if not os.path.exists(self.HHS_PUNCH_FILE):
            with open(self.HHS_PUNCH_FILE, 'w') as f_punch:
                f_punch.write(f"{date_stamp} => ")

        print('Punch')

        return self._exit_code


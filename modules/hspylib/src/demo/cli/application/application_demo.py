#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.application
      @file: application_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from core.tools.commons import sysout
from modules.cli.application.application import Application

APP_NAME = 'AppTest'

VERSION = (0, 1, 0)

USAGE = "AppTest [-i input] [-o output] <one|two|three> <anything>"

DESCRIPTION = "HsPyLib application Demo"

EPILOG = "This is just a simple application demo"


class Main(Application):

    def _setup_arguments(self) -> None:
        # @formatter:off
        self._with_options()\
                .option('output', 'o', 'output', 'the output file') \
                .option('input', 'i', 'input', 'the input file')
        self._with_arguments()\
                .argument('number', 'the number to be used', choices=['one', 'two', 'three']) \
                .argument('anything', 'any value')
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        self._exec_application()

    def _exec_application(self) -> None:
        if self.getarg('number') == 'one':
            sysout(f"One: {self.getarg('anything')}")
        elif self.getarg('number') == 'two':
            sysout(f"Two: {self.getarg('anything')}")
        elif self.getarg('number') == 'three':
            sysout(f"Three: {self.getarg('anything')}")
        sysout('Done')


if __name__ == "__main__":
    # Application entry point
    Main('AppTest', VERSION, DESCRIPTION, USAGE, EPILOG).INSTANCE.run(sys.argv[1:])

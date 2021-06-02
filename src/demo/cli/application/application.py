#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.cli.application
      @file: application.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import sys

from hspylib.core.tools.commons import sysout
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain

VERSION = (0, 1, 0)

USAGE = """
Usage: AppTest [-i input] [-o output] <one|two|three> <anything>
""".format()


class Main(Application):

    def _setup_parameters(self, *params, **kwargs) -> None:
        self._with_option('o', 'output', True, lambda arg: print(f'Option -o | --output = {arg}'))
        self._with_option('i', 'input', True, lambda arg: print(f'Option -i | --input = {arg}'))
        # @formatter:off
        self._with_arguments(
            ArgumentChain.builder()
                .when('number', 'one|two|three', False)
                .require('anything', '.+')
                .end()
                .build()
        )
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
    Main('AppTest', VERSION, USAGE).INSTANCE.run(sys.argv[1:])

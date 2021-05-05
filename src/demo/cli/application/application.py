#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.cli.application
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

    def setup_parameters(self, *params, **kwargs) -> None:
        self.with_option('o', 'output', True, lambda arg: print(f'Option -o | --output = {arg}'))
        self.with_option('i', 'input', True, lambda arg: print(f'Option -i | --input = {arg}'))
        # @formatter:off
        self.with_arguments(
            ArgumentChain.builder()
                .when('Number', 'one|two|three', False)
                .require('Anything', '.+')
                .end()
                .build()
        )
        # @formatter:on

    def main(self, *params) -> None:
        self._exec_application()

    def _exec_application(self) -> None:
        if 'one' == self.get_argument(0):
            sysout(f'One: {self.get_argument(1)}')
        elif 'two' == self.get_argument(0):
            sysout(f'Two: {self.get_argument(1)}')
        elif 'three' == self.get_argument(0):
            sysout(f'Three: {self.get_argument(1)}')
        else:
            sysout(f'INVALID => {str(self.args)}')
        sysout('Done')


if __name__ == "__main__":
    """Application entry point"""
    Main('AppTest', VERSION, USAGE).INSTANCE.run(sys.argv[1:])

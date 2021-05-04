#!/usr/bin/env python3
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
            sysout(f'One: {str(self.args)}')
        elif 'two' == self.get_argument(0):
            sysout(f'Two: {str(self.args)}')
        elif 'three' == self.get_argument(0):
            sysout(f'Three: {str(self.args)}')
        else:
            sysout(f'INVALID => {str(self.args)}')
        sysout('Done')


if __name__ == "__main__":
    """Application entry point"""
    Main('AppTest', VERSION, USAGE).INSTANCE.run(sys.argv[1:])

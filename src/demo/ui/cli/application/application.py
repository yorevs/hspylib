#!/usr/bin/env python3
import sys

from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.app.argument_chain import ArgumentChain

VERSION = (0, 1, 0)

USAGE = """
Usage: AppTest [-i input] [-o output] <one|two|three> <anything>
""".format()


class Main(Application):
    def main(self, *params):
        self.with_option('o', 'output', True, lambda arg: print(f'Option -o | --output = {arg}'))
        self.with_option('i', 'input', True, lambda arg: print(f'Option -i | --input = {arg}'))
        self.with_arguments(
            ArgumentChain.builder()
                .when('Number', 'one|two|three', False)
                    .require('Anything', '.+')
                    .end()
                .build()
        )
        self.parse_parameters(*params)
        self.exec_operation()

    def exec_operation(self):
        if 'list' == self.args[0]:
            sysout(f'List: {str(self.args)}')
        elif 'add' == self.args[0]:
            sysout(f'Add: {str(self.args)}')
        elif 'upd' == self.args[0]:
            sysout(f'Update: {str(self.args)}')
        elif 'del' == self.args[0]:
            sysout(f'Delete: {str(self.args)}')
        elif 'get' == self.args[0]:
            sysout(f'Get: {str(self.args)}')
        else:
            sysout(f'VALID => {str(self.args)}')
        sysout('Done')


if __name__ == "__main__":
    """Application entry point"""
    Main('AppTest', VERSION, USAGE).INSTANCE.run(sys.argv[1:])

import sys

from hspylib.core.tools.commons import sysout
from hspylib.ui.cli.app.application import Application

VERSION = (0, 1, 0)

USAGE = """
Usage: AppTest [-i input] [-o output] <one|two|three> <anything>
""".format()


class Main(Application):
    def main(self, *args):
        self.with_option('o', 'output', True, lambda arg: print(f'Option -o | --output = {arg}'))
        self.with_option('i', 'input', True, lambda arg: print(f'Option -i | --input = {arg}'))
        self.with_argument('Number', 'one|two|three')
        self.with_argument('Anything', '[a-z]{3,7}')
        self.parse_arguments(*args)
        sysout('Done')


if __name__ == "__main__":
    """Application entry point"""
    Main('AppTest', VERSION, USAGE).INSTANCE.run(sys.argv[1:])

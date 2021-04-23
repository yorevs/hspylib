import sys

from hspylib.ui.cli.app.application import Application

VERSION = (0, 1, 0)

USAGE = """
Usage: AppTest -i input -o output
""".format()


class Main(Application):
    def main(self, *args):
        self.with_option('o', 'output', True, lambda arg: print(f'Passed -o | --output = {arg}'), True)
        self.with_option('i', 'input', True, lambda arg: print(f'Passed -i | --input = {arg}'), True)
        self.parse_arguments(*args)


if __name__ == "__main__":
    """Application entry point"""
    Main('AppTest', VERSION, USAGE).INSTANCE.run(sys.argv[1:])

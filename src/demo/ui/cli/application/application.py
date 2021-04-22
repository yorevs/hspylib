import sys

from hspylib.ui.cli.appfw.application import Application


class Main(Application):
    def main(self, *args):
        self.with_option('o', 'output', 1, lambda: print('Passed -o output'))
        self.with_option('i', 'input', 1, lambda: print('Passed -i input'))
        self.parse_arguments(*args)


if __name__ == "__main__":
    """Application entry point"""
    Main('AppTest').INSTANCE.run(sys.argv[1:])

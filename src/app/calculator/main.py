#!/usr/bin/env python3
import os
import signal
import sys

from hspylib.ui.cli.app.application import Application
from calculator.core.qt_calculator import QtCalculator


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # Version tuple: (major,minor,build)
    VERSION = (0, 9, 0)

    # CloudFoundry manager usage message
    USAGE = """
    Usage: {} <option> [arguments]
""".format(APP_NAME)

    def __init__(self, app_name: str):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        super().__init__(app_name, self.VERSION, self.USAGE, source_dir)
        self.calc = QtCalculator()
        signal.signal(signal.SIGINT, self.exit_handler)

    def main(self, *args, **kwargs):
        self.calc.run()


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])

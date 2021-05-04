#!/usr/bin/env python3
import os
import sys

from calculator.core.qt_calculator import QtCalculator
from hspylib.core.tools.commons import dirname, read_version
from hspylib.modules.cli.application.application import Application


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # Version tuple: (major,minor,build)
    VERSION = (0, 9, 0)

    # CloudFoundry manager usage message
    USAGE = f"""
    Usage: {APP_NAME} <option> [arguments]"""

    def __init__(self, app_name: str):
        super().__init__(app_name, read_version(), self.USAGE, dirname(__file__))
        self.calc = QtCalculator()

    def main(self, *args, **kwargs):
        self.calc.show()


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])

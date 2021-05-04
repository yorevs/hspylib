#!/usr/bin/env python3
import os
import sys

from calculator.core.qt_calculator import QtCalculator
from hspylib.core.tools.commons import __curdir__, __version__
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
        super().__init__(app_name, __version__(), self.USAGE, __curdir__(__file__))
        self.calc = QtCalculator()

    def main(self, *args, **kwargs):
        self.calc.show()


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])

import os
import sys
from typing import List

from hspylib.core.tools.commons import __version__, __curdir__, sysout
from hspylib.ui.cli.app.application import Application


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # Usage message
    USAGE = f"Usage: {APP_NAME} <option> [arguments]"

    def __init__(self, app_name: str):
        super().__init__(app_name, __version__(), self.USAGE, __curdir__(__file__))

    def main(self, arguments: List[str]) -> None:
        """Run the application with the command line arguments"""
        sysout(f'Hello {self.APP_NAME}')


if __name__ == "__main__":
    """Application entry point"""
    Main('Application name').INSTANCE.run(sys.argv[1:])

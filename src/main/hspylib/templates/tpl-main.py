import os
import pathlib
import sys

from hspylib.core.tools.commons import __version__, __curdir__, sysout
from hspylib.modules.application.application import Application

# The directory containing this file
HERE = pathlib.Path(__file__).parent


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # The application version
    VERSION = __version__(f"{HERE}/.version")

    # Usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, __curdir__(__file__))

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        sysout(f'Hello {self.APP_NAME}')


if __name__ == "__main__":
    """Application entry point"""
    Main('Application name').INSTANCE.run(sys.argv[1:])

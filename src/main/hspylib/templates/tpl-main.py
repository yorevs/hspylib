import sys

from hspylib.core.tools.commons import __version__, __curdir__, sysout, __here__
from hspylib.modules.application.application import Application

HERE = __here__(__file__)


class Main(Application):
    """TODO"""

    # The application version
    VERSION = __version__(f"{HERE}/.version")

    # Usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    def __init__(self, app_name: str):
        # Invoke the super constructor without source_dir parameter to skip creation of log and properties
        super().__init__(app_name, self.VERSION, self.USAGE, source_dir=__curdir__(__file__))

    def setup_parameters(self, *params, **kwargs):
        """Initialize application parameters and options"""
        pass

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        sysout(f'Hello {self.app_name}')

    def cleanup(self):
        """Execute code cleanup before exiting"""
        pass


if __name__ == "__main__":
    """Application entry point"""
    Main('Application name').INSTANCE.run(sys.argv[1:])

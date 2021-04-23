#!/usr/bin/env python3
import os
import signal
import sys
import traceback
from datetime import datetime
from typing import List, Any

from cfman.core.cf_man import CFManager
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.menu.menu_utils import MenuUtils


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # CloudFoundry manager usage message
    USAGE = """
Usage: {} <option> [arguments]

    Cloud Foundry Manager v{} Manage PCF applications.

    Options:
      -v  |    --version                : Display current program version.
      -h  |       --help                : Display this help message.
      -a  |        --api <api_url>      : Set the API to connect to
      -o  |        --org <org_url>      : Set the organization to connect to
      -s  |      --space <space_url>    : Set the space to connect to
      -u  |   --username <username>     : Set the username
      -p  |   --password <password>     : Set the password
""".format(APP_NAME, '.'.join(map(str, Application.__version__())))

    WELCOME = """
    
{} v{}
"""

    def __init__(self, app_name: str):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        super().__init__(app_name, Application.__version__(), self.USAGE, source_dir)
        self.option_map = {}
        self.cfman = None
        signal.signal(signal.SIGINT, self.exit_handler)

    def main(self, arguments: List[str]) -> None:
        """Run the application with the command line arguments"""
        self.with_option('a', 'api', True, lambda arg: self.__add_option__('api', arg))
        self.with_option('o', 'org', True, lambda arg: self.__add_option__('org', arg))
        self.with_option('s', 'space', True, lambda arg: self.__add_option__('space', arg))
        self.with_option('u', 'username', True, lambda arg: self.__add_option__('username', arg))
        self.with_option('p', 'password', True, lambda arg: self.__add_option__('password', arg))
        self.parse_arguments(arguments)
        self.cfman = CFManager(self.option_map)
        self.configs.logger().info(
            self.WELCOME.format(
                self.app_name,
                Application.__version__(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.__exec_application__()

    def __add_option__(self, key: str, value: Any):
        self.option_map[key] = value

    def __exec_application__(self) -> None:
        """Execute the application"""
        try:
            self.cfman.run()
        except Exception:
            err = str(traceback.format_exc())
            self.configs.logger().error('Failed to execute PCF manager => {}'.format(err))
            MenuUtils.print_error('Failed to execute PCF manager => {}'.format(err))

    def __reqopts__(self) -> int:
        return 0


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])

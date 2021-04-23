#!/usr/bin/env python3
import os
import signal
import sys
import traceback
from datetime import datetime
from typing import List, Any

from cfman.core.cf_man import CFManager
# Application name, read from it's own file path
from hspylib.ui.cli.app.application import Application

APP_NAME = os.path.basename(__file__)

# Version tuple: (major,minor,build)
VERSION = (0, 9, 0)

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
""".format(APP_NAME, ' '.join(map(str, VERSION)))

WELCOME = """

HSPyLib Cloud Foundry Manager v{}
"""


class Main(Application):

    def __init__(self, app_name: str):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        super().__init__(app_name, VERSION, USAGE, source_dir)
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
            WELCOME.format(
                VERSION,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.__app_exec__()

    def __add_option__(self, key: str, value: Any):
        self.option_map[key] = value

    def __app_exec__(self) -> None:
        """Execute the application logic based on the specified operation"""
        try:
            self.cfman.run()
        except Exception as err:
            self.configs.logger().error('Failed to execute PCF manager => {}'.format(str(err)))
            traceback.print_exc()
            self.exit_handler(1)

    def __reqopts__(self) -> int:
        return 0


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])

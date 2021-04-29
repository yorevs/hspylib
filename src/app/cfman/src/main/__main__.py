#!/usr/bin/env python3
import logging as log
import os
import sys
import traceback
from datetime import datetime
from typing import List, Any

from cfman.src.main.core.cf_man import CFManager
from hspylib.core.tools.commons import __version__, __curdir__
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.menu.menu_utils import MenuUtils


class Main(Application):
    """Cloud Foundry Manager - Manage PCF applications."""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # The application version
    VERSION = __version__('src/main/.version')

    # CloudFoundry manager usage message
    USAGE = """
Usage: {} <option> [arguments]

    Cloud Foundry Manager v{} - Manage PCF applications.

    Options:
      -v  |    --version                : Display current program version.
      -h  |       --help                : Display this help message.
      -a  |        --api <api_url>      : Set the API to connect to
      -o  |        --org <org_url>      : Set the organization to connect to
      -s  |      --space <space_url>    : Set the space to connect to
      -u  |   --username <username>     : Set the username
      -p  |   --password <password>     : Set the password
""".format(APP_NAME, '.'.join(map(str, VERSION)))

    WELCOME = """
    
{} v{}
"""

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, __curdir__(__file__))
        self.option_map = {}
        self.cfman = None

    def main(self, arguments: List[str]) -> None:
        """Run the application with the command line arguments"""
        self.with_option('a', 'api', True, lambda arg: self.__add_option__('api', arg))
        self.with_option('o', 'org', True, lambda arg: self.__add_option__('org', arg))
        self.with_option('s', 'space', True, lambda arg: self.__add_option__('space', arg))
        self.with_option('u', 'username', True, lambda arg: self.__add_option__('username', arg))
        self.with_option('p', 'password', True, lambda arg: self.__add_option__('password', arg))
        self.parse_parameters(arguments)
        self.cfman = CFManager(self.option_map)
        log.info(
            self.WELCOME.format(
                self.app_name,
                self.VERSION,
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
            log.error('Failed to execute PCF manager => {}'.format(err))
            MenuUtils.print_error('Failed to execute PCF manager => {}'.format(err))


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Cloud Foundry Manager').INSTANCE.run(sys.argv[1:])

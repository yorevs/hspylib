#!/usr/bin/env python3
import getopt
import os
import signal
import sys
import traceback
from datetime import datetime
from typing import List

from cfman.core.cf_man import CFManager
from firebase.core.firebase import APP_NAME, VERSION
from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout

# Usage message

USAGE = """
Usage: {} <option> [arguments]

    Cloud Foundry Manager v{} Manage PCF applications.

    Options:
      -v  |    --version          : Display current program version.
      -h  |       --help          : Display this help message.
      -a  |        --api          : Set the API to connect to
      -u  |   --username          : Set the username
      -p  |   --password          : Set the password
      -o  |        --org          : Set the organization to connect to
      -s  |      --space          : Set the space to connect to
""".format(APP_NAME, ' '.join(map(str, VERSION)))

WELCOME = """

Cloud Foundry Manager v{}
"""


class Main(metaclass=Singleton):
    options_map = {}

    @staticmethod
    def usage(exit_code: int = 0) -> None:
        """Display the usage message and exit with the specified code ( or zero as default )
        :param exit_code: The application exit code
        """
        sysout(USAGE)
        Main.exit_app(exit_code, cls=False)

    @staticmethod
    def version() -> None:
        """Display the current program version and exit"""
        sysout('HSPyLib Vault v{}'.format('.'.join(map(str, VERSION))))
        Main.exit_app(cls=False)

    @staticmethod
    def exit_app(exit_code=0, frame=None, cls: bool = True) -> None:
        """Safely exit the application"""
        sysout(frame if frame else '', end='')
        if cls:
            sysout('%ED2%%HOM%')
        exit(exit_code)

    @staticmethod
    def parse_arguments(arguments: List[str]) -> None:
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param arguments: The list of program arguments passed on the command line
        """
        try:
            opts, args = getopt.getopt(arguments, 'vha:u:p:o:s:', [
                'version', 'help', 'api', 'username', 'password', 'org', 'space'
            ])

            for op, arg in opts:
                if op in ('-v', '--version'):
                    Main.version()
                elif op in ('-h', '--help'):
                    Main.usage()
                elif op in ('-a', '--api'):
                    Main.options_map['api'] = arg
                elif op in ('-u', '--username'):
                    Main.options_map['username'] = arg
                elif op in ('-p', '--password'):
                    Main.options_map['password'] = arg
                elif op in ('-o', '--org'):
                    Main.options_map['org'] = arg
                elif op in ('-s', '--space'):
                    Main.options_map['space'] = arg
                else:
                    assert False, '### Unhandled option: {}'.format(op)
        except getopt.GetoptError as err:
            sysout('%RED%### Unhandled operation: {}'.format(str(err)))
            Main.usage(1)
        except AssertionError as err:
            sysout('%RED%### {}'.format(str(err)))
            Main.usage(1)

    def __init__(self):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        resource_dir = '{}/resources'.format(source_dir)
        log_dir = '{}/log'.format(resource_dir)
        self.configs = AppConfigs(
            source_root=source_dir,
            resource_dir=resource_dir,
            log_dir=log_dir
        )
        self.configs.logger().info(self.configs)
        self.cfman = None

    def run(self, arguments: List[str]) -> None:
        """Run the application with the command line arguments"""
        self.parse_arguments(arguments)
        self.cfman = CFManager(Main.options_map)
        signal.signal(signal.SIGINT, self.cfman.exit_handler)
        self.configs.logger().info(
            WELCOME.format(
                VERSION,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        signal.signal(signal.SIGINT, self.cfman.exit_handler)
        self.__app_exec()

    def __app_exec(self) -> None:
        """Execute the application logic based on the specified operation"""
        self.__execute__()

    def __execute__(self) -> None:
        """Execute the application
        """
        try:
            self.cfman.run()
        except Exception as err:
            self.configs.logger().error('Failed to execute PCF manager => {}'.format(str(err)))
            traceback.print_exc()
            self.cfman.exit_handler(1)


if __name__ == "__main__":
    """Application entry point"""
    Main().INSTANCE.run(sys.argv[1:])
    Main.exit_app()

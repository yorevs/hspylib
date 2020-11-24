#!/usr/bin/env python
import getopt
import os
import signal
import sys
from datetime import datetime
from typing import List

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.meta.singleton import Singleton
from hspylib.core.tools.commons import sysout, get_or_default
from hspylib.ui.cli.menu_utils import MenuUtils
from vault.core.vault import Vault, APP_NAME, VERSION
from vault.core.vault_config import VaultConfig
from hspylib.ui.cli.tools.validator.argument_validator import ArgumentValidator

USAGE = """
Usage: {} <option> [arguments]

    HSPyLib Vault v{}

    Options:
      -v  |  --version                      : Display current program version.
      -h  |  --help                         : Display this help message.
      -a  |  --add <name> <hint> [password] : Add a password entry to the vault.
      -d  |  --del <name>                   : Remove a password entry from the vault.
      -u  |  --upd <name> <hint> [password] : Update a password entry from the vault.
      -l  |  --list [filters]               : List all password json_string or matching the given filter.

    Arguments:
      name      : The name of the vault entry. That will identify the entry (name).
      hint      : Any hint related to that vault entry.
      password  : The password of the vault entry. If not provided, further input will be required.
      filter    : Filter the vault json_string by name.
""".format(APP_NAME, '.'.join(map(str, VERSION)))

WELCOME = """

HSPyLib Vault v{}

Settings ==============================
        VAULT_USER: {}
        VAULT_FILE: {}
        STARTED: {}
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
            sysout('\033[2J\033[H')
        exit(exit_code)

    @staticmethod
    def parse_arguments(arguments: List[str]) -> None:
        """ Handle program arguments and options. Short opts: -<C>, Long opts: --<Word>
        :param arguments: The list of program arguments passed on the command line
        """
        try:
            opts, args = getopt.getopt(arguments, 'vhagdul', [
                'version', 'help', 'add', 'get', 'del', 'upd', 'list'
            ])

            if len(opts) == 0:
                Main.usage()

            for op, arg in opts:
                if op in ('-v', '--version'):
                    Main.version()
                elif op in ('-h', '--help'):
                    Main.usage()
                elif op in ('-a', '--add'):
                    Main.options_map['add'] = args if ArgumentValidator.validate_argument(args, 2) else None
                elif op in ('-g', '--get'):
                    Main.options_map['get'] = args if ArgumentValidator.validate_argument(args, 2) else None
                elif op in ('-d', '--del'):
                    Main.options_map['del'] = args if ArgumentValidator.validate_argument(args, 2) else None
                elif op in ('-u', '--upd'):
                    Main.options_map['upd'] = args if ArgumentValidator.validate_argument(args, 2) else None
                elif op in ('-l', '--list'):
                    Main.options_map['list'] = args
                else:
                    assert False, '### Unhandled option: {}'.format(op)
                break
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
        self.vault = Vault()
        signal.signal(signal.SIGINT, self.vault.exit_handler)

    def run(self, arguments: List[str]) -> None:
        """Run the application with the command line arguments"""
        self.parse_arguments(arguments)
        self.configs.logger().info(
            WELCOME.format(
                VERSION,
                VaultConfig.INSTANCE.vault_user(),
                VaultConfig.INSTANCE.vault_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        signal.signal(signal.SIGINT, self.vault.exit_handler)
        self.app_exec()

    def app_exec(self):
        """Execute the application logic based on the specified operation"""
        for op in Main.options_map:
            if not Main.options_map[op] is None:
                self.exec_operation(op)
                break

    def exec_operation(self, op):
        """Execute the specified operation
        :param op: The vault operation to execute
        """
        try:
            options = tuple(Main.options_map[op])
            self.vault.open()
            if "add" == op:
                self.vault.add(options[0], options[1], get_or_default(options, 2))
            elif "get" == op:
                self.vault.get(options[0])
            elif "del" == op:
                self.vault.remove(options[0])
            elif "upd" == op:
                self.vault.update(options[0], options[1], get_or_default(options, 2))
            elif "list" == op:
                self.vault.list(get_or_default(options, 0))
            else:
                sysout('%RED%### Unhandled operation: {}'.format(op))
                Main.usage(1)
            self.vault.close()
        except Exception as err:
            self.configs.logger().error('Failed to execute \'vault --{}\' => {}'.format(op, str(err)))
            MenuUtils.print_error('Failed to execute \'vault --{}\' => '.format(op), str(err))
            self.vault.exit_handler(1)

        MenuUtils.wait_enter()


if __name__ == "__main__":
    """Application entry point"""
    Main().INSTANCE.run(sys.argv[1:])
    Main.exit_app()

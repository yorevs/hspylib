#!/usr/bin/env python3
import os
import signal
import sys
import traceback
from datetime import datetime

from hspylib.core.tools.commons import sysout, get_or_default
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.menu.menu_utils import MenuUtils
from hspylib.ui.cli.tools.validator.argument_validator import ArgumentValidator
from vault.core.vault import Vault
from vault.core.vault_config import VaultConfig


class Main(Application):
    """TODO"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # Vault usage message
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
""".format(APP_NAME, '.'.join(map(str, Application.__version__())))

    # Welcome message
    WELCOME = """

    {} v{}

    Settings ==============================
            VAULT_USER: {}
            VAULT_FILE: {}
            STARTED: {}
    """

    def __init__(self, app_name: str):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        super().__init__(app_name, Application.__version__(), self.USAGE, source_dir)
        self.vault = Vault()
        signal.signal(signal.SIGINT, self.exit_handler)

    def main(self, *args, **kwargs) -> None:
        """Run the application with the command line arguments"""
        self.with_option('a', 'add', handler=lambda arg: self.__exec_operation__('add', 2))
        self.with_option('g', 'get', handler=lambda arg: self.__exec_operation__('get', 1))
        self.with_option('d', 'del', handler=lambda arg: self.__exec_operation__('del', 1))
        self.with_option('u', 'upd', handler=lambda arg: self.__exec_operation__('upd', 2))
        self.with_option('l', 'list', handler=lambda arg: self.__exec_operation__('list'))
        self.parse_arguments(*args)
        self.configs.logger().info(
            self.WELCOME.format(
                self.app_name,
                Application.__version__(),
                VaultConfig.INSTANCE.vault_user(),
                VaultConfig.INSTANCE.vault_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    def cleanup(self):
        self.vault.close()

    def __exec_operation__(self, op: str, req_args: int = 0) -> None:
        """Execute the specified operation
        :param op: The vault operation to execute
        :param req_args: Number of required arguments for the operation
        """
        try:
            self.args = tuple(ArgumentValidator.check_arguments(self.args, req_args))
            self.vault.open()
            if "add" == op:
                self.vault.add(self.args[0], self.args[1], get_or_default(self.args, 2))
            elif "get" == op:
                self.vault.get(self.args[0])
            elif "del" == op:
                self.vault.remove(self.args[0])
            elif "upd" == op:
                self.vault.update(self.args[0], self.args[1], get_or_default(self.args, 2))
            elif "list" == op:
                self.vault.list(get_or_default(self.args, 0))
            else:
                sysout('%RED%### Invalid operation: {}'.format(op))
                self.usage(1)
        except Exception:
            err = str(traceback.format_exc())
            self.configs.logger().error('Failed to execute \'vault --{}\' => {}'.format(op, err))
            MenuUtils.print_error('Failed to execute \'vault --{}\' => '.format(op), err)
        finally:
            self.vault.close()

    def __reqopts__(self) -> int:
        return 1


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Vault').INSTANCE.run(sys.argv[1:])

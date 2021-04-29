#!/usr/bin/env python3
import logging as log
import os
import sys
from datetime import datetime

from hspylib.core.tools.commons import get_or_default, __version__, __curdir__, syserr
from hspylib.ui.cli.app.application import Application
from hspylib.ui.cli.app.argument_chain import ArgumentChain
from vault.src.main.core.vault import Vault
from vault.src.main.core.vault_config import VaultConfig


class Main(Application):
    """HSPyLib Vault - Manage your secrets"""

    # The application name
    APP_NAME = os.path.basename(__file__)

    # The application version
    VERSION = __version__('src/main/.version')

    # Vault usage message
    USAGE = """
Usage: vault [options] <operation> <arguments>

    HSPyLib Vault v{} - Manage your secrets.

    Options:
      -v  |  --version      : Display current program version.
      -h  |  --help         : Display this help message.
    
    Operations:
      list [filter]                 : List all passwords or matching the given filter criteria, if specified.
      get <name>                    : Get a decoded vault entry, specified by <name>.
      del <name>                    : Delete a decoded vault entry, specified by <name>.
      add <name> <hint> [password]  : Add a new non existent vault entry.
      upd <name> <hint> [password]  : Update an existent vault entry.

    Arguments:
      filter    : Filter the vault json_string by name.
      name      : The name of the vault entry. That will identify the entry (name).
      hint      : Any hint related to that vault entry.
      password  : The password of the vault entry. If not provided, further input will be required.
""".format(APP_NAME, '.'.join(map(str, VERSION)))

    # Welcome message
    WELCOME = """

    {} v{}

    Settings ==============================
            VAULT_USER: {}
            VAULT_FILE: {}
            STARTED: {}
    """

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, __curdir__(__file__))
        self.vault = Vault()

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        # @formatter:off
        self.with_arguments(
            ArgumentChain.builder()
                .when('Operation', 'list')
                    .accept('Filter', '.+')
                    .end()
                .when('Operation', 'add|upd')
                    .require('Name', '.+')
                    .require('Hint', '.+')
                    .accept('Password', '.+')
                    .end()
                .when('Operation', 'del|get')
                    .require('Name', '.+')
                    .end()
                .build()
        )
        # @formatter:on
        self.parse_parameters(*params)
        log.info(
            self.WELCOME.format(
                self.app_name,
                self.VERSION,
                VaultConfig.INSTANCE.vault_user(),
                VaultConfig.INSTANCE.vault_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self._exec_operation()

    def cleanup(self):
        self.vault.close()

    def _exec_operation(self, ) -> None:
        """Execute the specified vault operation"""
        op = self.args[0]
        try:
            self.vault.open()
            if "add" == op:
                self.vault.add(self.args[1], self.args[2], get_or_default(self.args, 3))
            elif "get" == op:
                self.vault.get(self.args[1])
            elif "del" == op:
                self.vault.remove(self.args[1])
            elif "upd" == op:
                self.vault.update(self.args[1], self.args[2], get_or_default(self.args, 3))
            elif "list" == op:
                self.vault.list(get_or_default(self.args, 1))
            else:
                syserr('### Invalid operation: {}'.format(op))
                self.usage(1)
        finally:
            self.vault.close()


if __name__ == "__main__":
    """Application entry point"""
    Main('HSPyLib Vault').INSTANCE.run(sys.argv[1:])

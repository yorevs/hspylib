#!/usr/bin/env python3
import logging as log
import sys
from datetime import datetime

from hspylib.core.tools.commons import get_or_default, __version__, __curdir__, syserr, __here__
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain
from vault.src.main.core.vault import Vault
from vault.src.main.core.vault_config import VaultConfig

HERE = __here__(__file__)


class Main(Application):
    """HSPyLib Vault - Manage your secrets"""

    # The application version
    VERSION = __version__('src/main/.version')

    # Vault usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # Welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, __curdir__(__file__))
        self.vault = Vault()

    def setup_parameters(self, *params, **kwargs):
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

    def main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(
            self.WELCOME.format(
                self.app_name,
                self.VERSION,
                VaultConfig.INSTANCE.vault_user(),
                VaultConfig.INSTANCE.vault_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self._exec_application()

    def cleanup(self):
        self.vault.close()

    def _exec_application(self, ) -> None:
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

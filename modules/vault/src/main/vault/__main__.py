#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.app.vault.src.main
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import sys
from datetime import datetime

from hspylib.core.tools.commons import get_path, read_version, dirname, syserr
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.argument_chain import ArgumentChain
from core.vault import Vault
from core.vault_config import VaultConfig

HERE = get_path(__file__)


class Main(Application):
    """HSPyLib Vault - Manage your secrets"""

    # The application version
    VERSION = read_version(f"{HERE}/.version")

    # Vault usage message
    USAGE = (HERE / "usage.txt").read_text().format('.'.join(map(str, VERSION)))

    # Welcome message
    WELCOME = (HERE / "welcome.txt").read_text()

    def __init__(self, app_name: str):
        super().__init__(app_name, self.VERSION, self.USAGE, dirname(__file__))
        self.vault = Vault()

    def _setup_parameters(self, *params, **kwargs) -> None:
        # @formatter:off
        self._with_arguments(
            ArgumentChain.builder()
                .when('operation', 'list')
                    .accept('filter', '.+')
                    .end()
                .when('operation', 'add|upd')
                    .require('name', '.+')
                    .require('hint', '.+')
                    .accept('password', '.+')
                    .end()
                .when('operation', 'del|get')
                    .require('name', '.+')
                    .end()
                .build()
        )
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(
            self.WELCOME.format(
                self._app_name,
                self.VERSION,
                VaultConfig.INSTANCE.vault_user(),
                VaultConfig.INSTANCE.vault_file(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        self._exec_application()

    def _cleanup(self) -> None:
        self.vault.close()

    def _exec_application(self, ) -> None:
        """Execute the specified vault operation"""
        op = self.getarg('operation')
        try:
            if self.vault.open():
                if op == 'add':
                    self.vault.add(self.getarg('name'), self.getarg('hint'), self.getarg('password'))
                elif op == 'get':
                    self.vault.get(self.getarg('name'))
                elif op == 'del':
                    self.vault.remove(self.getarg('name'))
                elif op == 'upd':
                    self.vault.update(self.getarg('name'), self.getarg('hint'), self.getarg('password'))
                elif op == 'list':
                    self.vault.list(self.getarg('filter'))
                else:
                    syserr(f'### Invalid operation: {op}')
                    self.usage(1)
        finally:
            self.vault.close()


if __name__ == "__main__":
    # Application entry point
    Main('HSPyLib Vault').INSTANCE.run(sys.argv[1:])

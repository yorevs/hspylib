#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.src.main
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import signal
import sys
from datetime import datetime
from textwrap import dedent

from hspylib.core.tools.commons import get_path, syserr
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import AppVersion

from vault.core.vault import Vault
from vault.core.vault_config import VaultConfig

HERE = get_path(__file__)


class Main(Application):
    """HSPyLib Vault - Manage your secrets"""

    # The welcome message
    DESCRIPTION = (HERE / "welcome.txt").read_text()

    # location of the .version file
    VERSION_DIR = str(HERE)

    # The resources folder
    RESOURCE_DIR = str(HERE / "resources")

    def __init__(self, app_name: str):
        version = AppVersion.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=self.RESOURCE_DIR)
        self.vault = Vault()

    def _setup_arguments(self) -> None:
        # @formatter:off

        self._with_chained_args('operation', 'the Vault operation to process') \
            .argument('list', 'list all entries matching the given filter criteria, if specified') \
                .add_argument(
                    'filter', "filter the listed vault entries by it's name",
                    nargs='?', default=None) \
            .argument('get', 'get a vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
            .argument('del', 'delete an existing vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
            .argument('add', 'add a NEW UNIQUE vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
                .add_argument('hint', 'applicable hints related to that vault entry') \
                .add_argument(
                    'password',
                    'the password of the entry. If not provided, it will be prompted',
                    nargs='?', default=None) \
            .argument('upd', 'update an existing vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
                .add_argument('hint', 'applicable hints related to that vault entry') \
                .add_argument(
                    'password',
                    'the password of the entry. If not provided, it will be prompted',
                    nargs='?', default=None) \
        # @formatter:on

    def _main(self, *params, **kwargs) -> None:
        """Run the application with the command line arguments"""
        log.info(dedent('''
        {} v{}

        Settings ==============================
                VAULT_USER: {}
                VAULT_FILE: {}
                STARTED: {}
        ''').format(
            self._app_name, self._app_version,
            VaultConfig.INSTANCE.vault_user(),
            VaultConfig.INSTANCE.vault_file(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        signal.signal(signal.SIGINT, self._abort)
        signal.signal(signal.SIGTERM, self._abort)
        signal.signal(signal.SIGABRT, self._abort)

        self._exec_application()

    def _cleanup(self) -> None:
        """TODO"""
        self.vault.close()

    def _abort(self, signum=0, frame=None) -> None:
        """TODO"""
        self._cleanup()
        self.exit(signum, frame)

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
    Main('vault').INSTANCE.run(sys.argv[1:])

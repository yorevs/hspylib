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

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
import signal
import sys
from textwrap import dedent

from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import syserr
from hspylib.core.zoned_datetime import now
from hspylib.modules.cli.application.application import Application
from hspylib.modules.cli.application.version import Version

from vault.__classpath__ import _Classpath
from vault.core.vault import Vault
from vault.core.vault_config import VaultConfig
from vault.exception.exceptions import VaultOpenError


class Main(Application):
    """HSPyLib Vault - Manage your secrets"""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=str(Charset.UTF_8))

    # location of the .version file
    VERSION_DIR = _Classpath.source_path()

    # The resources folder
    RESOURCE_DIR = str(_Classpath.resource_path())

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=self.RESOURCE_DIR)
        self.vault = Vault(self.RESOURCE_DIR)

    def _setup_arguments(self) -> None:
        # @formatter:off
        self._with_chained_args('operation', 'the Vault operation to process') \
            .argument('list', 'list all entries matching the given filter criteria, if specified') \
                .add_argument('filter', "filter the listed vault entries by it's name", nargs='*') \
            .argument('get', 'get a vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
            .argument('del', 'delete an existing vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
            .argument('add', 'add a NEW UNIQUE vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
                .add_argument('hint', 'applicable hints related to that vault entry') \
                .add_argument('password', 'the password of the entry. If not provided, it will be prompted', nargs='?') \
            .argument('upd', 'update an existing vault entry') \
                .add_argument('name', 'the name of the vault entry which identifies it') \
                .add_argument('hint', 'applicable hints related to that vault entry') \
                .add_argument('password', 'the password of the entry. If not provided, it will be prompted', nargs='?') \
        # @formatter:on

    def _main(self, *params, **kwargs) -> int:
        """Run the application with the command line arguments"""
        log.info(dedent(f'''
        {self._app_name} v{self._app_version}

        Settings ==============================
                VAULT_USER: {VaultConfig.INSTANCE.vault_user}
                VAULT_FILE: {VaultConfig.INSTANCE.vault_file}
                STARTED: {now("%Y-%m-%d %H:%M:%S")}
        =======================================\n
        '''))

        signal.signal(signal.SIGINT, self._abort)
        signal.signal(signal.SIGTERM, self._abort)
        signal.signal(signal.SIGABRT, self._abort)
        signal.signal(signal.SIGHUP, self._abort)

        return self._exec_application()

    def _cleanup(self) -> None:
        """Close and lock the vault"""
        self.vault.close()
        unlocked = self.vault.configs.unlocked_vault_file
        if os.path.exists(unlocked):
            os.remove(unlocked)

    def _abort(self, signum=0, frame=None) -> None:
        """Securely abort the execution of vault"""
        self._cleanup()
        self.exit(signum, frame)

    def _exec_application(self, ) -> int:
        """Execute the specified vault operation"""
        ret_val, op = 0, self.get_arg('operation')
        with self.vault.open() as unlocked:
            if not unlocked:
                raise VaultOpenError("Unable to open/unlock vault")
            if op == 'add':
                self.vault.add(self.get_arg('name'), self.get_arg('hint'), self.get_arg('password'))
            elif op == 'get':
                self.vault.get(self.get_arg('name'))
            elif op == 'del':
                self.vault.remove(self.get_arg('name'))
            elif op == 'upd':
                self.vault.update(self.get_arg('name'), self.get_arg('hint'), self.get_arg('password'))
            elif op == 'list':
                self.vault.list(self.get_arg('filter'))
            else:
                ret_val = 1
                syserr(f'### Invalid operation: {op}')
                self.usage(1)

        return ret_val


if __name__ == "__main__":
    # Application entry point
    Main('vault').INSTANCE.run(sys.argv[1:])

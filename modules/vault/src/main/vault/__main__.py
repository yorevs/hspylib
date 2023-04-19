#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Vault
   @package: vault
      @file: __main__.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from clitt.core.tui.tui_application import TUIApplication
from hspylib.core.enums.charset import Charset
from hspylib.core.tools.commons import hook_exit_signals, syserr
from hspylib.core.zoned_datetime import now
from hspylib.modules.application.exit_status import ExitStatus
from hspylib.modules.application.version import Version
from textwrap import dedent
from vault.__classpath__ import _Classpath
from vault.core.vault import Vault
from vault.core.vault_config import VaultConfig
from vault.exception.exceptions import VaultOpenError

import logging as log
import os
import sys


class Main(TUIApplication):
    """HsPyLib Vault - Manage your secrets"""

    # The welcome message
    DESCRIPTION = _Classpath.get_source_path("welcome.txt").read_text(encoding=Charset.UTF_8.val)

    # location of the .version file
    VERSION_DIR = _Classpath.source_path()

    # The resources folder
    RESOURCE_DIR = str(_Classpath.resource_path())

    def __init__(self, app_name: str):
        version = Version.load(load_dir=self.VERSION_DIR)
        super().__init__(app_name, version, self.DESCRIPTION.format(version), resource_dir=self.RESOURCE_DIR)
        self.vault = Vault(self.RESOURCE_DIR)

    def _setup_arguments(self) -> None:
        # fmt: off
        self._with_chained_args('operation', 'the Vault operation to process') \
            .argument('list', 'list all entries matching the given filter criteria, if specified') \
                .add_parameter('filter', "filter the listed vault entries by it's name", nargs='*') \
            .argument('get', 'get a vault entry') \
                .add_parameter('name', 'the name of the vault entry which identifies it') \
            .argument('del', 'delete an existing vault entry') \
                .add_parameter('name', 'the name of the vault entry which identifies it') \
            .argument('add', 'add a NEW UNIQUE vault entry') \
                .add_parameter('name', 'the name of the vault entry which identifies it') \
                .add_parameter('hint', 'applicable hints related to that vault entry', nargs='?') \
                .add_parameter('password', 'the password of the entry. If not provided, it will be prompted',
                               nargs='?') \
            .argument('upd', 'update an existing vault entry') \
                .add_parameter('name', 'the name of the vault entry which identifies it') \
                .add_parameter('hint', 'applicable hints related to that vault entry', nargs='?') \
                .add_parameter('password', 'the password of the entry. If not provided, it will be prompted',
                               nargs='?')  # fmt: on

    def _main(self, *params, **kwargs) -> ExitStatus:
        """Run the application with the command line arguments"""
        log.info(
            dedent(
                f"""
        {self._app_name} v{self._app_version}

        Settings ==============================
                VAULT_USER: {VaultConfig.INSTANCE.vault_user}
                VAULT_FILE: {VaultConfig.INSTANCE.vault_file}
                STARTED: {now("%Y-%m-%d %H:%M:%S")}
        =======================================\n
        """
            )
        )

        hook_exit_signals(self._abort)

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

    def _exec_application(self) -> ExitStatus:
        """Execute the specified vault operation"""
        ret_val, op = 0, self.get_arg("operation")
        with self.vault.open() as unlocked:
            if not unlocked:
                raise VaultOpenError("Unable to open/unlock vault")
            if op == "add":
                self.vault.add(self.get_arg("name"), self.get_arg("hint"), self.get_arg("password"))
            elif op == "get":
                self.vault.get(self.get_arg("name"))
            elif op == "del":
                self.vault.remove(self.get_arg("name"))
            elif op == "upd":
                self.vault.update(self.get_arg("name"), self.get_arg("hint"), self.get_arg("password"))
            elif op == "list":
                self.vault.list(self.get_arg("filter"))
            else:
                ret_val = 1
                syserr(f"### Invalid operation: {op}")
                self.usage(ExitStatus.FAILED)

        return ExitStatus.of(ret_val)


if __name__ == "__main__":
    # Application entry point
    Main("vault").INSTANCE.run(sys.argv[1:])

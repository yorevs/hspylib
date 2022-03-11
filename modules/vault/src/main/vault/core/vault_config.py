#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.core
      @file: vault_config.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import getpass
import os

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.metaclass.singleton import Singleton


class VaultConfig(metaclass=Singleton):
    """Holds the vault configurations"""

    def __init__(self):
        self.configs = AppConfigs.INSTANCE

    def vault_user(self) -> str:
        """Return the vault user"""
        user = self.configs['hhs.vault.user']
        return user if user else os.getenv('USER', getpass.getuser())

    def passphrase(self) -> str:
        """Return the vault user passphrase"""
        return self.configs['hhs.vault.passphrase']

    def vault_file(self) -> str:
        """Return the locked vault filename"""
        file = self.configs['hhs.vault.file']
        return file if file else f"{os.getenv('HOME', os.getcwd())}/.vault"

    def unlocked_vault_file(self) -> str:
        """Return the unlocked vault filename"""
        return f"{self.vault_file()}.unlocked"

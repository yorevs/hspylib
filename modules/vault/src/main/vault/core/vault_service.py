#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.core
      @file: vault_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from typing import Optional

from hspylib.core.datasource.crud_service import CrudService

from vault.core.vault_config import VaultConfig
from vault.core.vault_repository import VaultRepository
from vault.entity.vault_entry import VaultEntry


class VaultService(CrudService[VaultEntry]):
    """Provides a CRUD service for the Vault application"""

    def __init__(self, vault_config: VaultConfig):
        super().__init__(VaultRepository(vault_config))

    def get_by_key(self, key: str) -> Optional[VaultEntry]:
        """Get aa vault entry using the specified key
        :param key: The vault key to find
        """
        return self.repository.find_by_key(key)

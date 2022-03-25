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

   Copyright 2021, HSPyLib team
"""

from typing import Optional

from hspylib.core.crud.crud_service import CrudService
from hspylib.core.metaclass.singleton import Singleton

from vault.core.vault_repository import VaultRepository
from vault.entity.vault_entry import VaultEntry


class VaultService(CrudService, metaclass=Singleton):
    """Provides a CRUD service for the Vault application"""

    def __init__(self):
        self.repository = VaultRepository()
        super().__init__(self.repository)

    def get_by_key(self, key: str) -> Optional[VaultEntry]:
        """Get aa vault entry using the specified key
        :param key: The vault key to find
        """
        return self.repository.find_by_key(key)

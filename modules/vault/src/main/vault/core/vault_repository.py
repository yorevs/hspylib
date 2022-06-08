#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.vault.core
      @file: vault_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import re
from typing import List, Optional

from hspylib.core.crud.file.file_repository import FileRepository

from vault.core.vault_config import VaultConfig
from vault.entity.vault_entry import VaultEntry


class VaultRepository(FileRepository):

    def __init__(self):
        self.db_file = VaultConfig.INSTANCE.unlocked_vault_file()
        super().__init__(self.db_file)

    def find_all(self, filters: str = None) -> List[VaultEntry]:
        """Find all vault entries using the specified filter
        :param filters: the filter to restrict the search for entries
        """
        self.storage.load()
        data = self.storage.data or []
        if data and filters:
            filtered = []
            for entry in data:
                for key in entry.values():
                    if re.search(filters, key, re.IGNORECASE):
                        filtered.append(self.dict_to_entity(entry))
                        break
            return filtered

        return [self.dict_to_entity(entry) for entry in data]

    def find_by_key(self, key: str) -> Optional[VaultEntry]:
        """Find a vault entry matching the specified by key
        :param key: the entry key to find
        """
        self.storage.load()
        if key:
            result = next((entry for entry in self.storage.data if key == entry['key']), None)
            return self.dict_to_entity(result) if result else None

        return None

    def dict_to_entity(self, row: dict) -> VaultEntry:
        """Convert a dict into a vault entry
        :param row:
        """
        return VaultEntry(
            row['uuid'],
            row['key'],
            row['name'],
            row['password'],
            row['hint'],
            row['modified'])

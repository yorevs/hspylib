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
from typing import Optional, Set

from hspylib.core.datasource.identity import Identity
from hspylib.core.datasource.sqlite.sqlite_repository import SQLiteRepository
from hspylib.core.tools.text_tools import quote

from vault.entity.vault_entry import VaultEntry


class VaultRepository(SQLiteRepository[VaultEntry]):

    @property
    def db_file(self) -> str:
        return self._config.db_file

    def find_by_key(self, key: str, fields: Set[str] = None) -> Optional[VaultEntry]:
        fields = '*' if not fields else ', '.join(fields)
        clause = f"key = {quote(key)}"
        sql = f"SELECT {fields} FROM {self.table_name()} WHERE " + clause
        result = next((e for e in self.execute(sql)[1]), None)

        return self.to_entity_type(result) if result else None

    def table_name(self) -> str:
        return 'VAULT_ENTRIES'

    def to_entity_type(self, entity_dict: dict | tuple) -> VaultEntry:
        if isinstance(entity_dict, dict):
            identity = Identity(VaultEntry.VaultId(entity_dict['uuid']))
            return VaultEntry(identity, **entity_dict)

        identity = Identity(VaultEntry.VaultId(entity_dict[0]))
        return VaultEntry(
            identity,
            uuid=entity_dict[0],
            key=entity_dict[1],
            name=entity_dict[2],
            password=entity_dict[3],
            hint=entity_dict[4],
            modified=entity_dict[5],
        )

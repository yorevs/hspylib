#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Vault
   @package: vault.core
      @file: vault_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from typing import Optional, Set

from datasource.identity import Identity
from datasource.sqlite.sqlite_repository import SQLiteRepository
from hspylib.core.tools.text_tools import quote

from vault.entity.vault_entry import VaultEntry


class VaultRepository(SQLiteRepository[VaultEntry]):
    @property
    def database(self) -> str:
        return self._config.database

    def find_by_key(self, key: str, fields: Set[str] = None) -> Optional[VaultEntry]:
        fields = "*" if not fields else ", ".join(fields)
        clause = f"key = {quote(key)}"
        sql = f"SELECT {fields} FROM {self.table_name()} WHERE {clause} ORDER BY key"
        result = next((e for e in self.execute(sql)[1]), None)

        return self.to_entity_type(result) if result else None

    def table_name(self) -> str:
        return "VAULT_ENTRIES"

    def to_entity_type(self, entity_dict: dict | tuple) -> VaultEntry:
        if isinstance(entity_dict, dict):
            return VaultEntry(Identity(VaultEntry.VaultId(entity_dict["uuid"])), **entity_dict)
        return VaultEntry(
            Identity(VaultEntry.VaultId(entity_dict[0])),
            uuid=entity_dict[0],
            key=entity_dict[1],
            name=entity_dict[2],
            password=entity_dict[3],
            hint=entity_dict[4],
            modified=entity_dict[5],
        )

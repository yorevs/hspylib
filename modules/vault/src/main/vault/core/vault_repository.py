#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Vault
   @package: vault.core
      @file: vault_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datasource.identity import Identity
from datasource.sqlite.sqlite_repository import SQLiteRepository
from typing import Optional, Set
from vault.core.vault_config import VaultConfig
from vault.domain.vault_entry import VaultEntry


class VaultRepository(SQLiteRepository[VaultEntry, VaultConfig]):
    """Provide CRUD operations for the Vault application."""

    @property
    def database(self) -> str:
        return self._config.database

    def find_by_key(self, key: str, fields: Set[str] = None) -> Optional[VaultEntry]:
        fields = "*" if not fields else ", ".join(fields)
        sql = f"SELECT {fields} FROM {self.table_name()} WHERE key = ? ORDER BY key"
        result = next((e for e in self.execute(sql, key=key)[1]), None)

        return self.to_entity_type(result) if result else None

    def exists(self, key: str) -> bool:
        sql = f"SELECT rowid FROM {self.table_name()} WHERE key = ?"
        result = next((e for e in self.execute(sql, key=key)[1]), None)

        return bool(result)

    def table_name(self) -> str:
        return "VAULT_ENTRIES"

    def to_entity_type(self, entity_dict: dict | tuple) -> VaultEntry:
        if isinstance(entity_dict, dict):
            return VaultEntry(Identity(VaultEntry.VaultId(entity_dict["uuid"])), **entity_dict)
        return VaultEntry(
            Identity(VaultEntry.VaultId(entity_dict[0])),
            entity_dict[1],
            entity_dict[2],
            entity_dict[3],
            entity_dict[4],
            entity_dict[5],
        )

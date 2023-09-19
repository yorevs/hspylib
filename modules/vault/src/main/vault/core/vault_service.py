#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Vault
   @package: vault.core
      @file: vault_service.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datasource.crud_service import CrudService
from hspylib.core.namespace import Namespace
from textwrap import dedent
from typing import List, Optional
from vault.core.vault_config import VaultConfig
from vault.core.vault_repository import VaultRepository
from vault.domain.vault_entry import VaultEntry


class VaultService(CrudService[VaultRepository, VaultEntry]):
    """Provides a CRUD service for the Vault application."""

    def __init__(self, vault_config: VaultConfig):
        super().__init__(VaultRepository(vault_config))

    def get_by_key(self, key: str) -> Optional[VaultEntry]:
        """Get a vault entry using the specified key.
        :param key: the vault key to find.
        """
        return self.repository.find_by_key(key)

    def exists(self, key: str) -> bool:
        """Return whether the key exists or not in the database
        :param key: the vault key to check.
        """
        return self.repository.exists(key)

    def list_by_key(self, filter_expr: List[str] = None) -> List[VaultEntry]:
        """Return a list of vault entries that matches the specified filters.
        :param filter_expr: the expression
        """
        filters = " or ".join([f"key like '%{f}%'" for f in filter_expr])
        return self.list(Namespace("Filters", by_key_like=filters), ["key", "modified"])

    def create_vault_db(self) -> None:
        """Create a brand new vault database file."""
        self.repository.execute(
            dedent(
                """
        CREATE TABLE IF NOT EXISTS "VAULT_ENTRIES"
        (
            uuid         TEXT       not null,
            key          TEXT       not null,
            name         TEXT       not null,
            password     TEXT       not null,
            hint         TEXT       not null,
            modified     TEXT       not null,

            CONSTRAINT UUID_pk PRIMARY KEY (uuid),
            CONSTRAINT KEY_uk UNIQUE (key)
        )
        """
            )
        )

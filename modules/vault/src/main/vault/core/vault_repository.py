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
import ast
import logging as log
import os
from typing import List, Optional

from hspylib.core.preconditions import check_state

from vault.core.vault_config import VaultConfig
from vault.entity.vault_entry import VaultEntry


class VaultRepository:

    @staticmethod
    def dict_to_entity(row: dict) -> VaultEntry:
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

    def __init__(self, config: VaultConfig) -> None:
        self._config = config
        self._storage = None

    @property
    def config(self) -> VaultConfig:
        return self._config

    @property
    def vault_file(self) -> str:
        return self.config.vault_file

    @property
    def unlocked_vault_file(self) -> str:
        return self.config.unlocked_vault_file

    def find_all(self, filters: str = None) -> List[VaultEntry]:
        """Find all vault entries using the specified filter
        :param filters: the filter to restrict the search for entries
        """
        self._load()
        if filters:
            filtered = []
            for entry in self._storage:
                if all(f.lower() in entry['key'].lower() for f in filters):
                    filtered.append(self.dict_to_entity(entry))
            return filtered

        return [self.dict_to_entity(entry) for entry in self._storage]

    def find_by_key(self, key: str) -> Optional[VaultEntry]:
        """Find a vault entry matching the specified by key
        :param key: the entry key to find
        """
        self._load()
        if self._storage and key:
            entry = next((e for e in self._storage if key == e['key']), None)
            return self.dict_to_entity(entry) if entry else None

        return None

    def save(self, entity: VaultEntry) -> None:
        """TODO"""
        self._load()
        with open(self.unlocked_vault_file, 'w') as f_unlocked:
            t_entity = next(((i, e) for i, e in enumerate(self._storage) if e['key'] == entity.name), None)
            if t_entity:
                self._storage[t_entity[0]] = entity
            else:
                self._storage.append(entity)
            log.debug(f"Saved {len(self._storage)} entries from vault file")
            f_unlocked.write(f"[{','.join([str(e) for e in self._storage])}]")

    def delete(self, entity: VaultEntry) -> None:
        """TODO"""
        self._load()
        with open(self.unlocked_vault_file, 'w') as f_unlocked:
            entry = next((e for e in self._storage if e['key'] == entity.name), None)
            self._storage.remove(entry)
            log.debug(f"{entry} removed from vault file")
            f_unlocked.write(f"[{','.join([str(e) for e in self._storage])}]")

    def _load(self) -> None:
        """TODO"""

        if not self._storage:
            check_state(os.path.exists(self.unlocked_vault_file),
                        f"Vault file '{self.vault_file}' does not exist or it is locked")
            with open(self.unlocked_vault_file) as f_unlocked:
                lines = ''.join(map(str.strip, f_unlocked.readlines()))
                if lines:
                    entries = ast.literal_eval(lines)
                    data = list(map(self.dict_to_entity, entries)) if entries else []
                    log.debug(f"Read {len(data)} entries from vault file")
                    self._storage = data
                else:
                    self._storage = []

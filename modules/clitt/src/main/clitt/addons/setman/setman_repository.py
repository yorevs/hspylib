#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: setman_repository.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from typing import Optional, Set

from datasource.identity import Identity
from datasource.sqlite.sqlite_repository import SQLiteRepository

from clitt.addons.setman.setman_entry import SetmanEntry


class SetmanRepository(SQLiteRepository[SetmanEntry]):
    """Provide CRUD operations for the Vault application."""

    @property
    def database(self) -> str:
        return self._config.database

    def find_by_name(self, name: str, fields: Set[str] = None) -> Optional[SetmanEntry]:
        fields = "*" if not fields else ", ".join(fields)
        sql = f"SELECT {fields} FROM {self.table_name()} WHERE name = ? ORDER BY name"
        result = next((e for e in self.execute(sql, name=name)[1]), None)

        return self.to_entity_type(result) if result else None

    def table_name(self) -> str:
        return "SETTINGS"

    def to_entity_type(self, entity_dict: dict | tuple) -> SetmanEntry:
        if isinstance(entity_dict, dict):
            return SetmanEntry(Identity(SetmanEntry.SetmanId(entity_dict["uuid"])), **entity_dict)
        return SetmanEntry(
            Identity(SetmanEntry.SetmanId(entity_dict[0])),
            entity_dict[1],
            entity_dict[2],
            entity_dict[3],
        )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: settings_repository.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from textwrap import dedent
from typing import List, Optional

from datasource.identity import Identity
from datasource.sqlite.sqlite_repository import SQLiteRepository

from setman.core.setman_enums import SettingsType
from setman.settings.settings_config import SettingsConfig
from setman.settings.settings_entry import SettingsEntry


class SettingsRepository(SQLiteRepository[SettingsEntry, SettingsConfig]):
    """Provide CRUD operations for the Settings."""

    @property
    def database(self) -> str:
        return self._config.database

    def find_by_name(self, name: str) -> Optional[SettingsEntry]:
        """Find settings by name."""
        sql = "SELECT * FROM SETTINGS WHERE name = ? ORDER BY name"
        result = next((e for e in self.execute(sql, name=name)[1]), None)

        return self.to_entity_type(result) if result else None

    def search(
        self, name: str | None = None, stype: SettingsType | None = None, limit: int = 500, offset: int = 0
    ) -> List[SettingsEntry]:
        """Search settings by settings type."""
        search_name = name.replace("*", "%") if name else "%"
        if stype:
            sql = f"SELECT * FROM SETTINGS WHERE name LIKE ? AND stype = ? ORDER BY name LIMIT {limit} OFFSET {offset}"
            result = self.execute(sql, name=search_name, stype=stype.val)[1] or []
        else:
            sql = f"SELECT * FROM SETTINGS WHERE name LIKE ? ORDER BY name LIMIT {limit} OFFSET {offset}"
            result = self.execute(sql, name=search_name)[1] or []

        return list(map(self.to_entity_type, result))

    def clear(self, name: str | None = None, stype: SettingsType | None = None) -> None:
        """Remove all settings matching prefix."""
        search_name = name.replace("*", "%") if name else "%"
        if stype:
            sql = "DELETE FROM SETTINGS WHERE name LIKE ? AND stype = ?"
            self.execute(sql, name=search_name, stype=stype.val)
        else:
            sql = "DELETE FROM SETTINGS WHERE name LIKE ?"
            self.execute(sql, name=search_name)

    def create_db(self) -> None:
        """Create the Settings database."""
        self.execute(
            dedent(
                """
                CREATE TABLE IF NOT EXISTS SETTINGS
                (
                    uuid         TEXT               not null,
                    name         TEXT               not null,
                    prefix       TEXT  default ""   not null,
                    value        TEXT  default ""   not null,
                    stype        TEXT               not null,
                    modified     TEXT               not null,

                    CONSTRAINT UUID_pk PRIMARY KEY (uuid),
                    CONSTRAINT NAME_uk UNIQUE (name)
                )
                """
            )
        )
        self.execute(
            dedent(
                """
                CREATE TABLE IF NOT EXISTS SETTINGS_EVENTS
                (
                    uuid         TEXT       not null,
                    event        TEXT       not null,
                    name         TEXT       not null,
                    old_value    TEXT       not null,
                    new_value    TEXT       not null,
                    created      TEXT       not null,

                    CONSTRAINT UUID_pk PRIMARY KEY (uuid)
                )
            """
            )
        )

    def table_name(self) -> str:
        return "SETTINGS"

    def to_entity_type(self, entity_dict: dict | tuple) -> SettingsEntry:
        if isinstance(entity_dict, dict):
            return SettingsEntry(Identity(SettingsEntry.SetmanId(entity_dict["uuid"])), **entity_dict)
        return SettingsEntry(
            Identity(SettingsEntry.SetmanId(entity_dict[0])),
            entity_dict[1],
            entity_dict[2],
            entity_dict[3],
            SettingsType.of_value(entity_dict[4]),
            entity_dict[5],
        )

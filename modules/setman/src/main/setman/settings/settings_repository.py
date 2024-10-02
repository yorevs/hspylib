#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Clitt
   @package: clitt.addons.setman
      @file: settings_repository.py
   @created: Mon, 5 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""
from typing import List, Optional

from datasource.identity import Identity
from datasource.sqlite.sqlite_repository import SQLiteRepository
from hspylib.core.preconditions import check_state
from setman.core.setman_enums import SettingsType
from setman.settings.setman_sqls import SETMAN_SQLS
from setman.settings.settings_config import SettingsConfig
from setman.settings.settings_entry import SettingsEntry


class SettingsRepository(SQLiteRepository[SettingsEntry, SettingsConfig]):
    """Provide CRUD operations for the Settings."""

    @property
    def database(self) -> str:
        return self._config.database

    def find_by_name(self, name: str) -> Optional[SettingsEntry]:
        """Find settings by name.
        :param name: The name of the settings to find.
        :return: An optional SettingsEntry that matches the given name, or None if not found.
        """
        sql = "SELECT * FROM SETTINGS WHERE name = ? ORDER BY name"
        result = next((e for e in self.execute(sql, name=name)[1]), None)

        return self.to_entity_type(result) if result else None

    def search(
        self, name: str | None = None, stype: SettingsType | None = None, limit: int = 500, offset: int = 0
    ) -> List[SettingsEntry]:
        """Search for settings entries based on the provided parameters.
        :param name: The name of the settings entry to search for.
        :param stype: The type of settings to filter by.
        :param limit: The maximum number of entries to return.
        :param offset: The number of entries to skip before starting to collect the result set.
        :return: A list of settings entries matching the search criteria.
        """
        search_name = name.replace("*", "%") if name else "%"
        if stype:
            sql = f"SELECT * FROM SETTINGS WHERE name LIKE ? AND stype = ? ORDER BY name LIMIT {limit} OFFSET {offset}"
            result = self.execute(sql, name=search_name, stype=stype.val)[1] or []
        else:
            sql = f"SELECT * FROM SETTINGS WHERE name LIKE ? ORDER BY name LIMIT {limit} OFFSET {offset}"
            result = self.execute(sql, name=search_name)[1] or []

        return list(map(self.to_entity_type, result))

    def clear(self, name: str | None = None, stype: SettingsType | None = None) -> int:
        """Clears settings from the database based on the provided name and type.
        :param name: Optional name of the setting to clear, with wildcard support. If not provided, matches all names.
        :param stype: Optional type of the setting to clear. If not provided, matches all types.
        :return: The number of settings cleared from the database.
        """
        search_name = name.replace("*", "%") if name else "%"
        if stype:
            sql: str = "DELETE FROM SETTINGS WHERE name LIKE ? AND stype = ?"
            count: int = self.execute(sql, name=search_name, stype=stype.val)
        else:
            sql: str = "DELETE FROM SETTINGS WHERE name LIKE ?"
            count: int = self.execute(sql, name=search_name)

        return count

    def create_db(self) -> None:
        """Create the Settings database tables."""
        result: list[str] = list()
        for sql in SETMAN_SQLS:
            result.append(self.execute(sql))
        check_state(len(result) > 0, "Unable to create all setman tables")

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

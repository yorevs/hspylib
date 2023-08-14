#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: clitt.addons.setman
      @file: settings.py
   @created: Thu, 04 Jul 2023
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from datasource.identity import Identity
from functools import lru_cache
from hspylib.core.preconditions import check_argument
from hspylib.core.tools.commons import dirname, file_is_not_empty, touch_file
from hspylib.core.tools.text_tools import ensure_endswith
from hspylib.core.zoned_datetime import now
from setman.core.setman_enums import SettingsType
from setman.settings.settings_config import SettingsConfig
from setman.settings.settings_entry import SettingsEntry
from setman.settings.settings_service import SettingsService
from typing import Any, List, Optional, Tuple

import csv
import logging as log
import os
import uuid


class Settings:
    """Class to provide settings interactions."""

    HEADERS = ["uuid", "name", "prefix", "value", "settings type", "modified"]

    def __init__(self, configs: SettingsConfig, preserve: bool = False) -> None:
        self._configs = configs
        self._preserve = preserve
        self._service = SettingsService(self.configs)
        if not file_is_not_empty(self.configs.database):
            self._create_db()
        self._limit = 500
        self._offset = 0

    def __str__(self):
        entries = f",{os.linesep}  ".join(list(map(str, self.search())))
        return f"Settings: [{os.linesep + '  ' if entries else ''}" f"{entries}" f"{os.linesep if entries else ''}]"

    def __repr__(self):
        return str(self)

    def __getitem__(self, name: str) -> SettingsEntry:
        return self.get(name)

    def __setitem__(self, name: str, item: Tuple[str, Any, SettingsType]) -> None:
        self.put(name, item[0], item[1], item[2])

    @property
    def configs(self) -> SettingsConfig:
        return self._configs

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, new_offset: int) -> None:
        self._offset = new_offset

    @property
    def preserve(self) -> bool:
        return self._preserve

    @preserve.setter
    def preserve(self, new_preserve: bool) -> None:
        self._preserve = new_preserve

    @lru_cache
    def get(self, name: str) -> Optional[SettingsEntry]:
        """Get setting matching the specified name.
        :param name the settings name to get.
        """
        if name:
            return self._service.get_by_name(name)
        return None

    def put(
        self,
        name: str | None = None,
        prefix: str | None = None,
        value: Any | None = None,
        stype: SettingsType | None = None
    ) -> Tuple[Optional[SettingsEntry], Optional[SettingsEntry]]:
        """Upsert the specified setting.
        :param name the settings name.
        :param prefix the settings prefix.
        :param value the settings value.
        :param stype the settings type.
        """
        if (found := self._service.get_by_name(name)) and self._preserve:
            log.debug("Setting preserved, and not overwritten: '%s'", found.name)
            return None, None
        entry = found or SettingsEntry(Identity(SettingsEntry.SetmanId(uuid.uuid4().hex)), name, prefix, value, stype)
        if any(a is None for a in [name, value, stype]):
            if not (entry := SettingsEntry.prompt(entry)):
                return None, None
        else:
            entry.prefix = prefix
            entry.stype = stype.val
            entry.value = value
        entry.modified = now()
        self._service.save(entry)
        log.debug("Setting saved: '%s'", entry.name)
        self._clear_caches()

        return found, entry

    def remove(self, name: str) -> Optional[SettingsEntry]:
        """Delete the specified setting.
        :param name the settings name to delete.
        """
        if name:
            found = self._service.get_by_name(name)
            if found:
                self._service.remove(found)
                self._clear_caches()
                return found
        return None

    @lru_cache(maxsize=500)
    def search(self, name: str | None = None, stype: SettingsType | None = None) -> List[SettingsEntry]:
        """Search all settings matching criteria.
        :param name the settings name to filter.
        :param stype the settings type to filter.
        """
        return self._service.search(name, stype, self.limit, self.offset)

    def clear(self, name: str | None = None, stype: SettingsType | None = None) -> None:
        """Clear all settings from the settings table.
        :param name the settings name to filter.
        :param stype the settings type to filter.
        """
        self._service.clear(name, stype)
        self._clear_caches()

    def import_csv(self, filepath: str) -> int:
        """Upsert settings from CSV file into the database.
        :param filepath the path of the CSV file to be imported.
        """
        count, csv_file = 0, ensure_endswith(filepath, ".csv")
        check_argument(os.path.exists(filepath), "CSV file does not exist: " + csv_file)
        with open(csv_file, encoding="UTF8") as f_csv:
            csv_reader = csv.reader(f_csv, delimiter=",")
            for row in csv_reader:
                if row == self.HEADERS:
                    continue
                uid, name, prefix, value, stype = \
                    str(row[0]), str(row[1]), str(row[2]), str(row[3]), SettingsType.of_value(row[4])
                found = self._service.get_by_name(name)
                if found and self._preserve:
                    continue
                entry = SettingsEntry(Identity(SettingsEntry.SetmanId(uid)), name, prefix, value, stype)
                self._service.save(entry)
                count += 1
            self._clear_caches()
            return count

    def export_csv(self, filepath: str, name: str = None, stype: SettingsType = None) -> int:
        """Export settings from CSV file into the database.
        :param filepath the path of the CSV file to be exported.
        :param name the settings name to filter.
        :param stype the settings type to filter.
        """
        dest_dir, csv_file = dirname(filepath), ensure_endswith(filepath, ".csv")
        check_argument(os.path.exists(dest_dir), "Destination dir does not exist: " + dest_dir)
        settings = self.search(name, stype)
        with open(csv_file, "w", encoding="UTF8") as f_csv:
            writer = csv.writer(f_csv, delimiter=",")
            writer.writerow(self.HEADERS)
            writer.writerows(list(map(lambda s: s.values, settings)))
            return len(settings)

    def as_environ(self, name: str | None) -> List[str]:
        """Return all settings formatted as bash export environment variables.
        :param name the settings name to filter.
        """
        data = self.search(name, SettingsType.ENVIRONMENT)
        return list(map(SettingsEntry.to_env_export, data))

    def _create_db(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self.configs.database)
        self._service.create_db()
        log.info("Settings file has been created")
        return os.path.exists(self.configs.database)

    def _clear_caches(self) -> None:
        """Remove all caches."""
        self.get.cache_clear()
        self.search.cache_clear()

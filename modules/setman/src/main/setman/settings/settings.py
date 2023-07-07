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
from hspylib.core.exception.exceptions import ApplicationError
from hspylib.core.preconditions import check_argument, check_state
from hspylib.core.tools.commons import dirname, file_is_not_empty, safe_delete_file, touch_file
from hspylib.core.tools.text_tools import ensure_endswith
from hspylib.core.zoned_datetime import now
from hspylib.modules.security.security import decode_file, encode_file
from setman.core.setman_enums import SettingsType
from setman.settings.settings_config import SettingsConfig
from setman.settings.settings_entry import SettingsEntry
from setman.settings.settings_service import SettingsService
from typing import Any, List, Optional, Tuple

import binascii
import contextlib
import csv
import logging as log
import os
import uuid


class Settings:
    """Class to provide settings interactions."""

    HEADERS = ["uuid", "name", "value", "settings type", "modified"]

    def __init__(self, configs: SettingsConfig) -> None:
        self._is_open = False
        self._configs = configs
        self._service = SettingsService(self.configs)
        if not file_is_not_empty(self.configs.database):
            self._create_db()
        self._limit = 500
        self._offset = 0

    def __str__(self):
        entries = f",{os.linesep}  ".join(list(map(lambda s: str(s), self.search())))
        return f"Settings: [{os.linesep + '  ' if entries else ''}" f"{entries}" f"{os.linesep if entries else ''}]"

    def __repr__(self):
        return str(self)

    def __getitem__(self, name: str) -> SettingsEntry:
        return self.get(name)

    def __setitem__(self, name: str, item: Tuple[Any, SettingsType]) -> None:
        self.upsert(name, item[0], item[1])

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
    def is_open(self) -> bool:
        return self._is_open

    @is_open.setter
    def is_open(self, new_is_open: bool) -> None:
        self._is_open = new_is_open
        log.debug(f"Settings database open: {self.configs.database}")

    @contextlib.contextmanager
    def open(self) -> None:
        """Decode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if not self.is_open:
                self.is_open = True
                if self.configs.is_db_encoded:
                    self._decode_db_file()
            yield self
        except (UnicodeDecodeError, binascii.Error) as err:
            err_msg = f"Failed to open settings file => {self.configs.database}"
            log.error(ApplicationError(err_msg, err))
            yield self
        except Exception as err:
            err_msg = f"Unable to close settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        finally:
            self.close()

    def close(self) -> None:
        """Encode and open the SQL lite database file. Return the context to manipulate it."""
        try:
            if self._is_open:
                if self.configs.is_db_encoded:
                    self._encode_db_file()
                self._is_open = False
                log.debug(f"Settings database closed: {self.configs.database}")
        except (UnicodeDecodeError, binascii.Error) as err:
            err_msg = f"Failed to close settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        except Exception as err:
            err_msg = f"Unable to close settings file => {self.configs.database}"
            raise ApplicationError(err_msg, err) from err
        finally:
            safe_delete_file(self.configs.encoded_db)
            safe_delete_file(self.configs.decoded_db)

    @lru_cache
    def get(self, name: str) -> Optional[SettingsEntry]:
        """Get setting matching the specified name.
        :param name: the settings name to get.
        """
        check_state(self.is_open, "Settings database is not open")
        if name:
            return self._service.get(name)
        return None

    def upsert(
        self, name: str | None = None, value: Any | None = None, stype: SettingsType | None = None
    ) -> Tuple[Optional[SettingsEntry], Optional[SettingsEntry]]:
        """Upsert the specified setting.
        :param name: the settings name.
        :param value: the settings value.
        :param stype: the settings type.
        """
        check_state(self.is_open, "Settings database is not open")
        found = self._service.get(name)
        entry = found or SettingsEntry(Identity(SettingsEntry.SetmanId(uuid.uuid4().hex)), name, value, stype)
        if not name or not value or not stype:
            entry = SettingsEntry.prompt(entry)
        if entry:
            entry.modified = now()
            self._service.save(entry)
            self._clear_caches()
        return found, entry

    def remove(self, name: str) -> Optional[SettingsEntry]:
        """Delete the specified setting.
        :param name: the settings name to delete.
        """
        check_state(self.is_open, "Settings database is not open")
        if name:
            found = self._service.get(name)
            if found:
                self._service.remove(found)
                self._clear_caches()
                return found
        return None

    @lru_cache(maxsize=500)
    def search(self, name: str | None = None, stype: SettingsType | None = None) -> List[SettingsEntry]:
        """Search all settings matching criteria.
        :param name: the settings name to filter.
        :param stype: the settings type to filter.
        """
        check_state(self.is_open, "Settings database is not open")
        return self._service.search(name, stype, self.limit, self.offset)

    def clear(self, name: str | None = None, stype: SettingsType | None = None) -> None:
        """Clear all settings from the settings table.
        :param name: the settings name to filter.
        :param stype: the settings type to filter.
        """
        check_state(self.is_open, "Settings database is not open")
        self._service.clear(name, stype)
        self._clear_caches()

    def import_csv(self, filepath: str) -> int:
        """Upsert settings from CSV file into the database.
        :param filepath: the path of the CSV file to be imported.
        """
        count, csv_file = 0, ensure_endswith(filepath, ".csv")
        check_argument(os.path.exists(filepath), "CSV file does not exist: " + csv_file)
        with open(csv_file, encoding="UTF8") as f_csv:
            csv_reader = csv.reader(f_csv, delimiter=",")
            for row in csv_reader:
                if row == self.HEADERS:
                    continue
                uid, name, value, stype = str(row[0]), str(row[1]), str(row[2]), SettingsType.of_value(row[3])
                entry = SettingsEntry(Identity(SettingsEntry.SetmanId(uid)), name, value, stype)
                self._service.save(entry)
                count += 1
            self._clear_caches()
            return count

    def export_csv(self, filepath: str, name: str = None, stype: SettingsType = None) -> int:
        """Export settings from CSV file into the database.
        :param filepath: the path of the CSV file to be exported.
        :param name: the settings name to filter.
        :param stype: the settings type to filter.
        """
        dest_dir, csv_file = dirname(filepath), ensure_endswith(filepath, ".csv")
        check_argument(os.path.exists(dest_dir), "Destination dir does not exist: " + dest_dir)
        settings = self.search(name, stype)
        with open(csv_file, "w", encoding="UTF8") as f_csv:
            writer = csv.writer(f_csv, delimiter=",")
            writer.writerow(self.HEADERS)
            writer.writerows(list(map(lambda s: s.values, settings)))
            return len(settings)

    def _create_db(self) -> bool:
        """Create the settings SQLite DB file."""
        touch_file(self.configs.database)
        self._service.create_db()
        log.info("Settings file has been created")
        self._is_open = True
        return os.path.exists(self.configs.database)

    def _encode_db_file(self) -> None:
        """Decode the Base64 encoded database file."""
        if file_is_not_empty(self.configs.database):
            encoded = f"{self.configs.database}-encoded"
            encode_file(self.configs.database, encoded, binary=True)
            os.rename(encoded, self.configs.database)
            log.debug("Settings file is encoded")

    def _decode_db_file(self) -> None:
        """Base64 encode the database file."""
        if file_is_not_empty(self.configs.database):
            decoded = f"{self.configs.database}-decoded"
            decode_file(self.configs.database, decoded, binary=True)
            os.rename(decoded, self.configs.database)
            log.debug("Settings file is decoded")

    def _clear_caches(self) -> None:
        """Remove all caches."""
        self.get.cache_clear()
        self.search.cache_clear()
